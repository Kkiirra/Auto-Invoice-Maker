from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from customuser.models import User_Account
from .models import Transaction
from accounts.models import Account
from company.models import Currency, Company
from contractors.models import Contractor
from dateutil.parser import parse
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from invoice.models import Invoice
from django.contrib.auth.decorators import login_required
from integrations.views import refresh_token
from integrations.models import Bank_Account
import requests


@login_required(login_url='/signin/')
def transactions_view(request):
    user_account = User_Account.objects.get(owner=request.user)

    if request.method == 'GET':
        companies = Company.objects.filter(user_account=user_account)
        if companies:
            transactions = Transaction.objects.filter(user_account=user_account).order_by('-transaction_date')  # '-transaction_type',
            if not request.GET.get('page') == 'all':
                paginator = Paginator(transactions, 8)
                page = request.GET.get('page')
                transactions = paginator.get_page(page)

            instances = ((transaction, Invoice.objects.filter(company=transaction.company, contractor=transaction.contractor))
                         for transaction in transactions)

            contractors = Contractor.objects.filter(user_account=user_account)
            currencies = Currency.objects.all()
            transactions_types = Transaction.transaction_types

            context = {'currencies': currencies, 'instances': instances, 'contractors': contractors,
                        'transactions_types': transactions_types, 'companies': companies, 'transactions': transactions}
            return render(request, 'transactions/transactions.html', context)


@login_required(login_url='/signin/')
def add_transaction(request):
    if request.method == 'POST':

        transaction_date = parse(request.POST.get('datetimes'), dayfirst=True)
        company_uid = request.POST.get('company_uid')
        account_uid = request.POST.get('account_uid')
        contractor_uid = request.POST.get('contractor_uid')
        transaction_amount = request.POST.get('transaction_amount')
        transaction_type = request.POST.get('type_transact')
        contractor_name = request.POST.get('contractor_name')


        user_account = User_Account.objects.get(owner=request.user)

        if contractor_name:
            contractor = Contractor.objects.create(contractor_name=contractor_name, user_account=user_account)
        else:
            try:
                contractor = Contractor.objects.get(uid=contractor_uid)
            except ValidationError:
                contractor = Contractor.objects.create(contractor_name=contractor_uid, user_account=user_account)
        company = Company.objects.get(uid=company_uid, user_account=user_account)
        account = Account.objects.get(uid=account_uid, user_account=user_account)
        new_transaction = Transaction.objects.create(account=account, company=company,
                                                     contractor=contractor,
                                                     sum_of_transactions=transaction_amount,
                                                     transaction_type=transaction_type,
                                                     user_account=user_account, transaction_date=transaction_date)

        return HttpResponseRedirect('/transactions/')



@login_required(login_url='/signin/')
def delete_transaction(request):

    user_account = User_Account.objects.filter(owner=request.user)
    uid = request.POST.get('uid')
    try:
        transaction = Transaction.objects.filter(user_account=user_account[0], uid=uid)

        if transaction:
            pre_invoice = transaction[0].invoice
            transaction[0].delete()
            pre_invoice.save()

        return JsonResponse({}, status=200)

    except Exception:
        return redirect('customuser:bad_request')


@login_required(login_url='/signin/')
def transaction_edit(request, tr_uid):
    user_account = User_Account.objects.filter(owner=request.user)
    if request.method == 'GET':
        if user_account:
            user_account = user_account[0]
            transaction = Transaction.objects.get(user_account=user_account, uid=tr_uid)
            contractors = Contractor.objects.filter(user_account=user_account)
            companies = Company.objects.filter(user_account=user_account)
            user_invoices = Invoice.objects.filter(user_account=user_account, contractor=transaction.contractor,
                                              company=transaction.company, account=transaction.account)
            currencies = Currency.objects.all()
            transaction_types = Transaction.transaction_types
            selected_invoice = transaction.invoice
            return render(request, 'transactions/transaction_edit.html', {'transaction': transaction,
                                                                          'accounts': transaction.company.accounts.all(),
                                                                          'contractors': contractors,
                                                                          'currencies': currencies, 'user_invoices': user_invoices,
                                                                          'transaction_types': transaction_types,
                                                                          'companies': companies, 'selected_invoice': selected_invoice})
    else:

        user_account = User_Account.objects.filter(owner=request.user)[0]
        transaction = Transaction.objects.filter(uid=tr_uid, user_account=user_account)

        company_uid = request.POST.get('company_uid')
        account_uid = request.POST.get('account_uid')
        contractor_uid = request.POST.get('contractor_uid')
        transaction_amount = request.POST.get('transaction_amount')
        transaction_date = parse(request.POST.get('datetimes'), dayfirst=True)
        invoices = request.POST.getlist('invoices[]')
        company = Company.objects.get(user_account=user_account, uid=company_uid)
        account = Account.objects.get(uid=account_uid, user_account=user_account, company=company)
        transaction.update(company=company, account=account, sum_of_transactions=transaction_amount, transaction_date=transaction_date)

        transaction_relation = transaction[0].invoice
        if transaction_relation:

            if (transaction_relation.company != transaction_relation.company) or (transaction_relation.account != transaction_relation.account)\
                    or (transaction_relation.contractor != transaction_relation.contractor):
                transaction_relation.invoice.remove(transaction_relation)

        for invoice_uid in invoices:
            new_invoice = Invoice.objects.get(uid=invoice_uid)

            transaction_relation.invoice.add(new_invoice)

            transaction_relation.save()


        if contractor_uid:
            contractor = Contractor.objects.filter(uid=contractor_uid, user_account=user_account)[0]
            transaction.update(contractor=contractor)

        return HttpResponseRedirect(f'/transactions/{tr_uid}/')


@login_required(login_url='/signin/')
def get_invoice_val(request):
    context = {}
    user_account = User_Account.objects.get(owner=request.user)
    company = Company.objects.get(user_account=user_account, uid=request.POST.get('company'))
    contractor = Contractor.objects.get(user_account=user_account, uid=request.POST.get('contractor'))
    account = Account.objects.get(user_account=user_account, uid=request.POST.get('account'))

    invoice = Invoice.objects.filter(contractor=contractor, account=account, company=company)
    for index in invoice:
        context[index.__str__()] = index.uid
    return JsonResponse(context, status=200)


@login_required(login_url='/signin/')
def get_transaction_company(request):
    context = {}
    company = Company.objects.get(uid=request.POST.get('company'))
    for index in company.accounts.all():
        context[f'{index.currency} - {index.account_id} - {index.bank}'] = index.uid
    return JsonResponse(context, status=200)


@login_required(login_url='/signin/')
def delete_invoice(request):
    user_account = User_Account.objects.get(owner=request.user)
    transaction_uid = request.POST.get('transaction_uid')
    transaction = Transaction.objects.get(user_account=user_account, uid=transaction_uid)
    invoice = transaction.invoice
    transaction.invoice = None
    transaction.save()
    invoice.save()

    return JsonResponse({}, status=200)


def add_invoice(request):
    user_account = User_Account.objects.get(owner=request.user)

    invoice_uid = request.POST.get('invoice_uid')
    transaction_uid = request.POST.get('transaction_uid')

    transaction = Transaction.objects.get(user_account=user_account, uid=transaction_uid)
    pre_invoice = transaction.invoice
    invoice = Invoice.objects.get(user_account=user_account, uid=invoice_uid)

    transaction.invoice = invoice
    transaction.save()
    transaction.invoice.save()

    if pre_invoice is not None:
        pre_invoice.save()

    return JsonResponse({}, status=200)


def load_transactions(request):
    access_token = refresh_token()
    user_account = User_Account.objects.get(owner=request.user)
    bank_accounts = Bank_Account.objects.filter(user_account=user_account)
    for index in bank_accounts:
        accounts = index.data['accounts']
        if accounts:
            for bank_account_uid, data in accounts[0].items():
                print(bank_account_uid, data)

                user_transactions = requests.get(
                    url=f'https://ob.nordigen.com/api/v2/accounts/{bank_account_uid}/transactions/',
                    headers={'accept': 'application/json',
                             'Authorization': f'Bearer {access_token}'})

                user_transactions_response = user_transactions.json()
                account = Account.objects.get(user_account=user_account, uid=data['account_uid'])
                company = Company.objects.get(user_account=user_account, uid=data['company_uid'])

                for transaction_info in user_transactions_response['transactions']['booked']:
                    if transaction_info:

                        transaction_id = transaction_info.get('transactionId')

                        if not Transaction.objects.filter(transaction_id=transaction_id, user_account=user_account):

                            transaction_amount = transaction_info['transactionAmount']['amount']
                            creation_date = transaction_info['bookingDate']
                            transaction_date = transaction_info['valueDate']

                            if float(transaction_amount) < 0 and not transaction_info.get('creditorName') is None:
                                transaction_type = 'Expenses'
                                contractor_name = transaction_info.get('creditorName')

                                if not contractor_name:
                                    contractor_name = transaction_info.get('debtorName')
                                    if not contractor_name:
                                        contractor_name = company.company_name

                            else:
                                transaction_type = 'Income'
                                contractor_name = transaction_info.get('debtorName')

                                if not contractor_name:
                                    contractor_name = transaction_info.get('creditorName')
                                    if not contractor_name:
                                        contractor_name = company.company_name

                            try:
                                contractor = Contractor.objects.get(contractor_name=contractor_name,
                                                                    user_account=user_account)
                            except Exception:
                                contractor = Contractor.objects.create(contractor_name=contractor_name,
                                                                       user_account=user_account)

                            transaction = Transaction.objects.create(transaction_id=transaction_id, user_account=user_account,
                                                       account=account, contractor=contractor,
                                                       sum_of_transactions=abs(float(transaction_amount)),
                                                       transaction_type=transaction_type,
                                                       transaction_date=transaction_date,
                                                       creation_date=creation_date, company=company)
                            if transaction_type == 'Income':
                                invoices = Invoice.objects.filter(user_account=user_account, company=company,
                                                                  account=account, contractor=contractor,
                                                                  invoice_sum__gte=abs(float(transaction_amount)),
                                                                  invoice_date__gte=transaction_date)

                                if invoices:
                                    transaction.invoice = invoices[0]
                                    transaction.save()
                                    transaction.invoice.save()

    return JsonResponse({}, status=200)

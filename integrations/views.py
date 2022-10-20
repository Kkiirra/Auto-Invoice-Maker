from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from random import randint
import requests

from company.models import Company
from .models import Bank_Account
from accounts.models import Account
from contractors.models import Contractor
from customuser.models import User_Account
from transactions.models import Transaction
from invoice.models import Invoice


def refresh_token():
    get_access = requests.post(url='https://ob.nordigen.com/api/v2/token/new/',
                               headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                               json={'secret_id': 'bd5516c3-3bfd-4f1a-828e-a5a0b9e7d58c',
                                     'secret_key': '10c6d6126ae3557a18ed905359633a246df6566ff5a047f82fd3dde3d7f9176b91ba5b0178228b8b9e9d3e90a39de563e2973a4c536f8958317ea81493dba2f1'})
    access_token = get_access.json()['access']
    return access_token


@login_required(login_url='/signin/')
def integrations_view(request):
    user_language = request.LANGUAGE_CODE.upper()
    reference = randint(1000, 1000000)
    user_account = User_Account.objects.get(owner=request.user)



    access_token = refresh_token()


    if request.method == 'POST':
        this_banks = request.POST.get('bank').split('/')
        bank = this_banks[0]
        max_days = this_banks[1]
        access_token = request.session.get('access_token')

        if access_token is None:
            get_access = requests.post(url='https://ob.nordigen.com/api/v2/token/new/',
                                       headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                                       json={'secret_id': 'bd5516c3-3bfd-4f1a-828e-a5a0b9e7d58c',
                                             'secret_key': '10c6d6126ae3557a18ed905359633a246df6566ff5a047f82fd3dde3d7f9176b91ba5b0178228b8b9e9d3e90a39de563e2973a4c536f8958317ea81493dba2f1'})
            access_token = get_access.json()['access']
            request.session['access_token'] = access_token
        else:
            access_token = request.session['access_token']

        r = requests.post(url='https://ob.nordigen.com/api/v2/agreements/enduser/',
                          headers={'accept': 'application/json', 'Content-Type': 'application/json',
                                   'Authorization': f'Bearer {access_token}'},
                          json={'institution_id': bank, 'max_historical_days': max_days, 'access_valid_for_days': 90,
                                'access_scope': ['transactions']})
        print(r.json())
        agreement = r.json()['id']

        user_agreement = requests.post(url='https://ob.nordigen.com/api/v2/requisitions/',
                                       headers={'accept': 'application/json', 'Content-Type': 'application/json',
                                                'Authorization': f'Bearer {access_token}'},
                                       json={'redirect': f'http://app.finum.online/integration-response/?bank={r.json()["institution_id"]}',
                                             'institution_id': bank, 'reference': reference,
                                             'agreement': agreement, 'user_language': user_language})
        user_login_token = user_agreement.json()
        bank_account, created = Bank_Account.objects.get_or_create(user_account=user_account,
                                                                   name=user_login_token['institution_id'])
        if created:
            bank_account.data = {
                'agreement_id': user_login_token['id'],
                'institution_id': user_login_token['institution_id'],
                'agreement': user_login_token['agreement'],
                'accounts': [{index: {}} for index in user_login_token['accounts']],
            }
        else:
            bank_account.data['agreement_id'] = user_login_token['id']
            bank_account.data['agreement'] = user_login_token['agreement']
        bank_account.save()
        request.session['agreement_id'] = user_login_token['id']
        return JsonResponse({'href': user_login_token['link']}, status=200)
    else:
        context = {}
        banks_accounts = user_account.bank_account.all()

        for index in banks_accounts:
            context[index.name] = []
            for account in index.data['accounts']:
                account = list(account.keys())[0]
                user_transactions = requests.get(url=f'https://ob.nordigen.com/api/v2/accounts/{account}',
                                                 headers={'accept': 'application/json',
                                                          'Authorization': f'Bearer {access_token}'})
                iban = user_transactions.json()['iban']
                try:
                    created_account = Account.objects.get(user_account=user_account, account_id=iban)
                except Exception:
                    created_account = None

                if not created_account:
                    status = user_transactions.json()['status']
                    context[index.name].append({'account': {'iban': iban, 'status': status, 'account_id': account}})
                else:
                    context[index.name].append({'account': {'iban': iban, 'status': 'CREATED', 'account_id': account,
                                                            'company': created_account.company}})

        return render(request, 'integrations/integrations.html', context)


@login_required(login_url='/signin/')
def integrations_response(request):
    user_account = User_Account.objects.get(owner=request.user)
    bank_account = Bank_Account.objects.get(user_account=user_account, name=request.GET.get('bank'))
    agreement_id = bank_account.data['agreement_id']
    access_token = refresh_token()

    get_user_accounts = requests.get(url=f'https://ob.nordigen.com/api/v2/requisitions/{agreement_id}/',
                                     headers={'accept': 'application/json', 'Content-Type': 'application/json',
                                              'Authorization': f'Bearer {access_token}'})
    print(get_user_accounts.json())
    user_accounts = get_user_accounts.json()['accounts']

    for index in user_accounts:
        bank_account.data['accounts'].append({index: {}})
    bank_account.save()

    return HttpResponseRedirect('/integrations/')


@login_required(login_url='/signin/')
def integrate_account(request):
    if request.method == 'POST':
        user_account = User_Account.objects.get(owner=request.user)

        access_token = refresh_token()


        bank_account_uid = request.POST.get('account')
        company_name = request.POST.get('company')
        bank_name = request.POST.get('bank').strip()
        account_number = request.POST.get('account_iban').strip()
        bank_account = Bank_Account.objects.get(user_account=user_account, data__accounts=[{bank_account_uid: {}}])

        company, status = Company.objects.get_or_create(user_account=user_account, company_name=company_name)

        user_transactions = requests.get(url=f'https://ob.nordigen.com/api/v2/accounts/{bank_account_uid}/transactions/',
                                         headers={'accept': 'application/json',
                                                  'Authorization': f'Bearer {access_token}'})

        user_transactions_response = user_transactions.json()

        if user_transactions_response.get('status_code') == 429:
            return JsonResponse(data={}, status=429)
        currency = user_transactions_response['transactions']['booked'][0]['transactionAmount']['currency']

        new_account = Account.objects.create(account_id=account_number, user_account=user_account, company=company,
                                             bank=bank_name, currency=currency)

        bank_account.data['accounts'][0][bank_account_uid].update({'account_uid': f'{new_account.uid}',
                                                                         'company_uid': f'{company.uid}'})
        bank_account.save()
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
                                contractor_name = company_name

                    else:
                        transaction_type = 'Income'
                        contractor_name = transaction_info.get('debtorName')

                        if not contractor_name:
                            contractor_name = transaction_info.get('creditorName')
                            if not contractor_name:
                                contractor_name = company_name


                    try:
                        contractor = Contractor.objects.get(contractor_name=contractor_name, user_account=user_account)
                    except Exception:
                        contractor = Contractor.objects.create(contractor_name=contractor_name, user_account=user_account)

                    Transaction.objects.create(transaction_id=transaction_id, user_account=user_account,
                                                                 account=new_account, contractor=contractor,
                                                                 sum_of_transactions=abs(float(transaction_amount)),
                                                                 transaction_type=transaction_type,
                                                                 transaction_date=transaction_date,
                                                                 creation_date=creation_date, company=company)

        return JsonResponse(data={'company_name': company_name}, status=200)


def add_invoices(request):

    user_account = User_Account.objects.get(owner=request.user)
    transactions = Transaction.objects.filter(user_account=user_account, transaction_type='Income')

    for transaction in transactions:
        invoices = Invoice.objects.filter(user_account=user_account, company=transaction.company,
                                          account=transaction.account, contractor=transaction.contractor,
                                          invoice_sum__gte=transaction.sum_of_transactions,
                                          invoice_date__gte=transaction.transaction_date)

        if invoices:
            transaction.invoice = invoices[0]
            transaction.save()
            transaction.invoice.save()
    return JsonResponse({}, status=200)

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from company.models import Company, Currency, Bank
from .models import Account
from customuser.models import User_Account


@login_required(login_url='/signin/')
def company_add_account(request, com_uid):
    """Добавление счёта на странице выбранной компании profile/company/<int:com_id>/ с возвращением на страницу
    этой компании"""
    if request.method == 'POST':

        account_id = request.POST.get('account_id')
        account_description = request.POST.get('account_description')
        bank = request.POST.get('bank_name')
        currency_name = request.POST.get('currency_name')

        user_account = User_Account.objects.get(owner=request.user)
        this_company = Company.objects.filter(uid=com_uid, user=request.user)

        new_account = Account.objects.create(account_id=account_id, bank=bank, company=this_company[0],
                                          currency=currency_name, user_account=user_account,
                                             account_description=account_description)
        return HttpResponseRedirect(f'/profile/companies/{com_uid}/')


@login_required(login_url='/signin/')
def add_accounts(request, com_uid):
    """Добавление счёта на странице profile/companies с помощью pop-up"""
    if request.method == 'POST':

        account = request.POST.get('account_id')
        bank = request.POST.get('bank_name')
        currency_name = request.POST.get('currency_name')
        print(account, bank, currency_name)
        user_account = User_Account.objects.get(owner=request.user)
        this_company = Company.objects.filter(uid=com_uid, user=request.user)
        new_account = Account.objects.create(account_id=account, bank=bank, company=this_company[0],
                                          currency=currency_name, user_account=user_account)
        return HttpResponseRedirect('/profile/companies/')
    else:
        print('DSAHFASFHDFHS')


@login_required(login_url='/signin/')
def accounts(request):
    """Добавление счёта на странице счетов profile/accounts"""
    currency = Currency.objects.all()
    banks = Bank.objects.all()
    if request.method == 'GET':

        user_account = User_Account.objects.filter(owner=request.user)

        if user_account:
            companies = Company.objects.filter(user_account=user_account[0])
            accounts = Account.objects.filter(user_account=user_account[0])
            return render(request, 'accounts/account.html', context={'currencies': currency,
                                                                     'accounts': accounts,
                                                                     'banks': banks, 'companies': companies})
        else:
            return redirect('company:start_company')

    else:
        company_uid = request.POST.get('company_uid')
        account_id = request.POST.get('account_id')
        account_description = request.POST.get('account_description')
        bank = request.POST.get('bank_name')
        currency_name = request.POST.get('currency_name')


        user_account = User_Account.objects.get(owner=request.user)
        this_company = Company.objects.filter(user=request.user)

        new_account = Account.objects.create(account_id=account_id, bank=bank, company=this_company[0],
                                              currency=currency_name, user_account=user_account,
                                             account_description=account_description)
        return HttpResponseRedirect('/profile/accounts/')


@login_required(login_url='/signin/')
def delete_account(request):
    """Удаление счета на странице счетов"""
    accounts_uid = request.POST.get('uid')
    user_account = User_Account.objects.filter(owner=request.user)
    account = Account.objects.filter(user_account=user_account[0], uid=accounts_uid)
    account.delete()
    return JsonResponse({}, status=200)



@login_required(login_url='/signin/')
def delete_this_account(request, com_uid, ac_uid):
    """Удаление счета на странице выбранной компании с возвращением на неё"""
    try:
        company = Company.objects.filter(user=request.user, uid=com_uid)
        get_account = Account.objects.filter(uid=ac_uid, company=company[0])
        get_account[0].delete()
        return HttpResponseRedirect(f'/profile/companies/{com_uid}/')
    except Exception:
        return redirect('customuser:bad_request')


def account_edit(request, ac_uid):

    account = Account.objects.filter(uid=ac_uid)
    currencies = Currency.objects.all()
    banks = Bank.objects.all()

    if account[0].company.user == request.user:

        if request.method == 'GET':
            if account:
                return render(request, 'accounts/account_edit.html', {'account': account[0],
                                                                      'company': account[0].company,
                                                                      'currencies': currencies,
                                                                      'banks': banks})
            else:
                return redirect('customuser:bad_request')
        else:
            account_id = request.POST.get('new_account_id')
            account_description = request.POST.get('account_description')
            new_bank = request.POST.get('bank_name')
            currency_name = request.POST.get('currency_name')
            account.update(account_id=account_id, bank=new_bank, currency=currency_name,
                           account_description=account_description)
            return HttpResponseRedirect(f'/profile/accounts/{ac_uid}/')

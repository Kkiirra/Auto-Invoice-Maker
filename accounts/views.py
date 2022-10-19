from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from company.models import Company, Currency, Bank
from .models import Account
from customuser.models import User_Account
from django.db import IntegrityError
from .forms import AccountForm


@login_required(login_url='/signin/')
def accounts(request):
    """Add account on profile/accounts/"""

    user_account = User_Account.objects.get(owner=request.user)
    companies = Company.objects.filter(user_account=user_account)
    accounts = Account.objects.filter(user_account=user_account)

    form = AccountForm(user_account)

    currency = Currency.objects.all()
    banks = Bank.objects.all()

    if request.method == 'POST':
        form = AccountForm(user_account, request.POST)

        if form.is_valid():
            form.instance.user_account = user_account

            try:
                form.save()
            except IntegrityError:
                form.add_error('account_id', 'Account with this ID already exists')

    context = {'currencies': currency, 'accounts': accounts, 'banks': banks, 'companies': companies, 'form': form}

    return render(request, 'accounts/account.html', context)


@login_required(login_url='/signin/')
def account_edit(request, ac_uid):
    """Edit company fields profile/accounts/uid"""
    user_account = User_Account.objects.get(owner=request.user)

    account = Account.objects.get(user_account=user_account, uid=ac_uid)
    companies = Company.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()
    banks = Bank.objects.all()

    if request.method == 'POST':
        form = AccountForm(user_account, request.POST, instance=account)

        if form.is_valid():
            form.save()
            return redirect('accounts:account_edit', account.uid)

    else:
        form = AccountForm(user_account, instance=account)

    context = {'account': account, 'companies': companies, 'currencies': currencies, 'banks': banks, 'form': form}

    return render(request, 'accounts/account_edit.html', context)


@login_required(login_url='/signin/')
def delete_account(request):
    """Delete account by uid/user_account on profile/accounts"""

    Account.objects.filter(
        user_account=User_Account.objects.get(owner=request.user), uid=request.POST.get('uid')).delete()

    return JsonResponse({}, status=200)

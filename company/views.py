from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
from accounts.forms import AccountForm
from customuser.models import User_Account
from .models import Company, Currency, Bank
from accounts.models import Account
from .forms import CompanyForm


@login_required(login_url='/signin/')
def companies_list(request):
    """The Page for creating companies/accounts"""
    user_account = User_Account.objects.get(owner=request.user)
    companies = Company.objects.filter(user_account=user_account)
    currency = Currency.objects.all()
    banks = Bank.objects.all()

    form = AccountForm(user_account)
    company_form = CompanyForm()

    if 'account_id' in request.POST:
        form = AccountForm(user_account, request.POST)

        if form.is_valid():
            form.instance.user_account = user_account

            try:
                form.save()
            except IntegrityError:
                form.add_error('account_id', 'Account with this ID already exists')

    elif 'company_name' in request.POST:
        company_form = CompanyForm(request.POST)

        if company_form.is_valid():
            company_form.instance.user_account = user_account

            try:
                company_form.save()
            except IntegrityError:
                company_form.add_error('company_name', 'Company with this name already exists')


    context = {'companies': companies, 'currencies': currency, 'banks': banks,
               'form': form, 'company_form': company_form}

    return render(request, 'company/companies.html', context)


@login_required(login_url='/signin/')
def company_edit(request, com_uid):
    """The Page for creating accounts and edit company settings"""

    user_account = User_Account.objects.get(owner=request.user)
    currency = Currency.objects.all()
    banks = Bank.objects.all()

    companies = Company.objects.filter(user_account=user_account)
    company = Company.objects.get(uid=com_uid, user_account=user_account)
    accounts = Account.objects.filter(company=company)

    form = AccountForm(user_account)
    company_form = CompanyForm()

    if 'account_id' in request.POST:
        form = AccountForm(user_account, request.POST)

        if form.is_valid():
            form.instance.user_account = user_account

            try:
                form.save()
            except IntegrityError:
                form.add_error('account_id', 'Account with this ID already exists')

    elif 'company_name' in request.POST:
        company_form = CompanyForm(request.POST, instance=company)

        if company_form.is_valid():
            company_form.instance.user_account = user_account

            try:
                company_form.save()
            except IntegrityError:
                company_form.add_error('company_name', 'Company with this name already exists')
            else:
                return redirect('company:this_company', company.uid)

    context = {'companies': companies, 'currencies': currency, 'form': form, 'company_form': company_form,
                   'company': company, 'accounts': accounts, 'banks': banks}

    return render(request, 'company/company_edit.html', context)


@login_required(login_url='/signin/')
def delete_company(request):
    Company.objects.filter(
        user_account=User_Account.objects.get(owner=request.user), uid=request.POST.get('uid')).delete()
    return JsonResponse({}, status=200)

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from customuser.models import User_Account
from .models import Company, Currency, Bank
from accounts.models import Account


@login_required(login_url='/signin/')
def companies_list(request):

    currency = Currency.objects.all()
    banks = Bank.objects.all()

    if request.method == 'GET':
        try:
            companies = Company.objects.filter(user=request.user)
            return render(request, 'company/companies.html', context={'companies': companies,
                                                                      'currencies': currency, 'banks': banks})
        except Exception:
            return redirect('customuser:bad_request')
    else:

        user_account = User_Account.objects.get(owner=request.user)
        company = request.POST.get('company_name')
        Company.objects.create(company_name=company, user=request.user, user_account=user_account)

        return HttpResponseRedirect('/profile/companies/')


@login_required(login_url='/signin/')
def delete_company(request):
    get_user_account = User_Account.objects.filter(owner=request.user)
    if get_user_account:
        uid = request.POST.get('uid')
        get_company = Company.objects.filter(user_account=get_user_account[0], uid=uid)
        if get_company:
            get_company[0].delete()
            return JsonResponse({}, status=200)
        else:
            redirect('customuser:bad_request')
    else:
        redirect('customuser:bad_request')


@login_required(login_url='/signin/')
def this_company(request, com_uid):

    currency = Currency.objects.all()
    banks = Bank.objects.all()

    try:
        company = Company.objects.filter(uid=com_uid, user=request.user)
    except:
        return redirect('customuser:bad_request')


    if request.method == 'GET':
        accounts = Account.objects.filter(company=company[0])
        context = {'companies': company, 'currencies': currency,
                   'company': company[0], 'accounts': accounts, 'banks': banks}

        return render(request, 'company/company_edit.html', context)
    else:

        new_company_name = request.POST.get('new_company_name')
        company.update(company_name=new_company_name)

        return HttpResponseRedirect(f'/profile/companies/{com_uid}/')


@login_required(login_url='/signin/')
def start_company(request):
    company = Company.objects.filter(user=request.user)
    if company:
        return redirect('company:dashboard')
    else:
        return render(request, 'company/start_company.html')
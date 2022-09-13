from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from customuser.models import User_Account
from .models import Order, Order_status
from company.models import Company, Currency
from contractors.models import Contractor
from dateutil.parser import parse
from django.core.exceptions import ValidationError


@login_required(login_url='/signin/')
def orders_view(request):
    statuses = Order_status.objects.all()
    currencies = Currency.objects.all()
    user_account = User_Account.objects.filter(owner=request.user)[0]
    companies = Company.objects.filter(user_account=user_account)

    if companies:
        orders = Order.objects.filter(user_account=user_account)
        contractors = Contractor.objects.filter(user_account=user_account)
        return render(request, 'orders/order.html', {'orders': orders, 'companies': companies,
                                                     'contractors': contractors,
                                                     'currencies': currencies, 'statuses': statuses})
    else:
        return redirect('company:start_company')


@login_required(login_url='/signin/')
def delete_order(request):

    user_account = User_Account.objects.filter(owner=request.user)
    ord_uid = request.POST.get('uid')

    try:
        order = Order.objects.filter(uid=ord_uid, user_account=user_account[0])[0]
        order.delete()
        return JsonResponse({}, status=200)
    except Exception:
        return redirect('customuser:bad_request')


@login_required(login_url='/signin/')
def add_order(request):
    if request.method == 'POST':

        order_name = request.POST.get('order_name')
        company_uid = request.POST.get('company_uid')
        contractor_uid = request.POST.get('contractor_uid')
        order_amount = request.POST.get('order_amount')
        currency = request.POST.get('currency_name')
        contractor_name = request.POST.get('contractor_name')
        order_date = parse(request.POST.get('datetimes'), dayfirst=True)

        user_account = User_Account.objects.get(owner=request.user)
        company = Company.objects.get(uid=company_uid, user_account=user_account)

        if contractor_name:
            contractor = Contractor.objects.create(user_account=user_account, contractor_name=contractor_name)
        else:
            try:
                contractor = Contractor.objects.get(uid=contractor_uid)
            except ValidationError:
                contractor = Contractor.objects.create(contractor_name=contractor_uid, user_account=user_account)

        new_order = Order.objects.create(order_name=order_name,
                                        company=company, contractor=contractor, order_sum=order_amount,
                                        currency=currency, user_account=user_account, order_date=order_date)
        return HttpResponseRedirect('/orders/')


@login_required(login_url='/signin/')
def order_edit(request, ord_uid):
    if request.method == 'GET':
        user_account = User_Account.objects.get(owner=request.user)

        order = Order.objects.get(uid=ord_uid, user_account=user_account)
        companies = Company.objects.filter(user_account=user_account)
        contractors = Contractor.objects.all()
        currencies = Currency.objects.all()

        context = {'order': order, 'currencies': currencies, 'companies': companies, 'contractors': contractors}

        return render(request, 'orders/order_edit.html', context)
    else:

        new_order_name = request.POST.get('new_order_name')
        currency_name = request.POST.get('currency_name')
        order_sum = request.POST.get('order_sum')
        company_uid = request.POST.get('company_uid')
        contractor_uid = request.POST.get('contractor_uid')
        order_date = parse(request.POST.get('datetimes'), dayfirst=True)

        order = Order.objects.filter(uid=ord_uid)
        company = Company.objects.filter(uid=company_uid)[0]
        contractor = Contractor.objects.filter(uid=contractor_uid)[0]

        order.update(order_name=new_order_name, currency=currency_name, order_sum=order_sum,
                     company=company, contractor=contractor, order_date=order_date)
        return HttpResponseRedirect(f'/orders/{ord_uid}/')

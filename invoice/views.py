from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from dateutil.parser import parse
import random
from accounts.models import Account
from company.models import Company, Currency
from contractors.models import Contractor
from customuser.models import User_Account
from orders.models import Order
from products.models import Product
from django.core.exceptions import ValidationError
from .models import Invoice, InvoiceItem, Invoice_status


@login_required(login_url='/signin/')
def invoice(request):
    user_account = User_Account.objects.get(owner=request.user)
    invoices = Invoice.objects.filter(user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    contractors = Contractor.objects.filter(user_account=user_account)
    invoice_stats = Invoice_status.objects.all()
    currencies = Currency.objects.all()
    return render(request, 'invoice/invoice.html', {'invoices': invoices, 'companies': companies, 'contractors': contractors,
                                                    'currencies': currencies, 'invoice_stats': invoice_stats})


@login_required(login_url='/signin/')
def delete_invoice(request):
    user_account = User_Account.objects.filter(owner=request.user)

    inv_uid = request.POST.get('uid')

    try:
        invoice = Invoice.objects.get(uid=inv_uid, user_account=user_account[0])
        invoice.delete()
        return JsonResponse({}, status=200)
    except Exception:
        return redirect('customuser:bad_request')


@login_required(login_url='/signin/')
def invoice_add(request):

    user_account = User_Account.objects.get(owner=request.user)


    if request.method == 'GET':

        products = Product.objects.filter(user_account=user_account)
        companies = Company.objects.filter(user_account=user_account)
        contractors = Contractor.objects.filter(user_account=user_account)
        orders = Order.objects.filter(user_account=user_account)
        currencies = Currency.objects.all()

        context = {'currencies': currencies, 'companies': companies, 'contractors': contractors, 'orders': orders,
                   'products': products}

        return render(request, 'invoice/invoice_add.html', context)
    else:

        invoice_total = float(request.POST.get('invoice_total'))
        currency = request.POST.get('currency_name')
        contractor_uid = request.POST.get('contractor_uid')
        company_uid = request.POST.get('company_uid')
        account_uid = request.POST.get('account_uid')
        order_uid = request.POST.get('order_name')
        invoice_status = request.POST.get('radio')
        invoice_date = parse(request.POST.get('datetimes'), dayfirst=True)

        try:
            invoice_last = Invoice.objects.latest('creation_date')
            invoice_number = int(invoice_last.invoice_name) + 1

        except Exception:
            invoice_number = random.randint(20000, 30000)

        try:
            invoice_flag = Invoice.objects.get(user_account=user_account, invoice_name=invoice_number)
        except Exception:
            invoice_flag = False

        if invoice_flag:
            context = {'invoice_name_error': 'The same number is exist, please, enter the new'}
        else:
            context = {}

            quantities = request.POST.getlist('quantity[]')
            products = request.POST.getlist('select_item')
            prices = request.POST.getlist('price[]')

            company = Company.objects.get(user_account=user_account, uid=company_uid)
            account = Account.objects.get(user_account=user_account, uid=account_uid, company=company)
            status = Invoice_status.objects.get(status=invoice_status)

            try:
                order = Order.objects.get(user_account=user_account, uid=order_uid)
            except ValidationError:
                order = None

            try:
                contractor = Contractor.objects.get(user_account=user_account, uid=contractor_uid)
            except ValidationError:
                contractor = Contractor.objects.create(user_account=user_account, contractor_name=contractor_uid)



            new_invoice = Invoice.objects.create(user_account=user_account, company=company, currency=currency,
                                                 contractor=contractor, invoice_name=invoice_number, invoice_sum=invoice_total,
                                                 invoice_date=invoice_date, order=order, account=account, invoice_status=status)
            for product, price, quantity in zip(products, prices, quantities):
                print(prices)
                try:
                    product = Product.objects.get(uid=product)
                except ValidationError:
                    product = Product.objects.create(user_account=user_account, product_name=product,
                                                         product_price=price, currency=currency)

                invoice_item = InvoiceItem.objects.create(user_account=user_account, product=product, invoice=new_invoice,
                                                      quantity=int(quantity), price=float(price))

        if invoice_flag:
            return render(request, 'invoice/invoice_add.html', context)
        else:
            return HttpResponseRedirect('/invoice/')


@login_required(login_url='/signin/')
def invoice_edit(request, inv_uid):

    user_account = User_Account.objects.get(owner=request.user)
    products = Product.objects.filter(user_account=user_account)
    invoice = Invoice.objects.get(uid=inv_uid, user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    orders = Order.objects.filter(user_account=user_account)
    contractors = Contractor.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()
    context = {'orders': orders, 'currencies': currencies, 'companies': companies, 'contractors': contractors,
               'products': products, 'invoice': invoice}
    if request.method == 'GET':


        return render(request, 'invoice/invoice_edit.html', context)

    else:
        invoice_total = float(request.POST.get('invoice_total'))
        items = request.POST.getlist('item[]')
        currency = request.POST.get('currency_name')
        contractor_uid = request.POST.get('contractor_uid')
        invoice_number = request.POST.get('invoice_number')
        company_uid = request.POST.get('company_uid')
        account_uid = request.POST.get('account_uid')
        invoice_date = parse(request.POST.get('datetimes'), dayfirst=True)
        order_uid = request.POST.get('order_name')
        quantities = request.POST.getlist('quantity[]')  # quantity_new
        products = request.POST.getlist('select_item')  # select_item_new
        prices = request.POST.getlist('price[]')  # price_new


        quantities_new = request.POST.getlist('quantity_new')
        products_new = request.POST.getlist('select_item_new')
        prices_new = request.POST.getlist('price_new')
        company = Company.objects.get(user_account=user_account, uid=company_uid)
        account = Account.objects.get(user_account=user_account, uid=account_uid, company=company)

        try:
            contractor = Contractor.objects.get(user_account=user_account, uid=contractor_uid)
        except ValidationError:
            contractor = Contractor.objects.create(user_account=user_account, contractor_name=contractor_uid)

        try:
            order = Order.objects.get(user_account=user_account, uid=order_uid)
        except ValidationError:
            order = None

        invoice = Invoice.objects.filter(user_account=user_account, uid=inv_uid)
        invoice.update(user_account=user_account, company=company, currency=currency, account=account,
                                                 contractor=contractor, invoice_name=invoice_number, invoice_sum=invoice_total,
                                                 invoice_date=invoice_date, order=order)

        for item, product, price, quantity in zip(items, products, prices, quantities):

            invoice_item = InvoiceItem.objects.filter(user_account=user_account, uid=item)

            try:
                product = Product.objects.filter(uid=product)
                product = product[0]
            except ValidationError:
                product = Product.objects.create(user_account=user_account, product_name=product,
                                                     product_price=price, currency=currency)
            invoice_item.update(product=product, quantity=quantity, price=price)

        if quantities_new is not None and prices_new is not None and products_new is not None:
            for product, price, quantity in zip(products_new, prices_new, quantities_new):
                try:
                    product = Product.objects.get(uid=product)
                except ValidationError:
                    product = Product.objects.create(user_account=user_account, product_name=product,
                                                     product_price=price, currency=currency)

                invoice_item = InvoiceItem.objects.create(user_account=user_account, product=product, invoice=invoice[0],
                                                      quantity=int(quantity), price=price)

    return HttpResponseRedirect(f'/invoice/{inv_uid}/')


@login_required(login_url='/signin/')
def invoice_byOrder(request, ord_uid):
    user_account = User_Account.objects.get(owner=request.user)
    products = Product.objects.filter(user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    orders = Order.objects.filter(user_account=user_account)
    selected_order = Order.objects.get(user_account=user_account, uid=ord_uid)
    contractors = Contractor.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()
    context = {'orders': orders, 'currencies': currencies, 'companies': companies, 'contractors': contractors,
               'products': products, 'invoice': invoice, 'selected_order': selected_order}
    return render(request, 'invoice/invoice_byorder.html', context)


@login_required(login_url='/signin/')
def change_status(request):
    status = request.POST.get('status')
    invoice_uid = request.POST.get('invoice')
    new_status = Invoice_status.objects.get(status=status)

    Invoice.objects.filter(uid=invoice_uid).update(invoice_status=new_status)


    return JsonResponse({}, status=200)

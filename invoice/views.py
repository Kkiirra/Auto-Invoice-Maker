from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from dateutil.parser import parse
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist
from company.models import Company, Currency
from contractors.models import Contractor
from customuser.models import User_Account
from orders.models import Order
from products.models import Product
from django.core.exceptions import ValidationError
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm
from django.db.models import Avg, Sum


@login_required(login_url='/signin/')
def invoice(request):
    user_account = User_Account.objects.get(owner=request.user)
    invoices = list()
    companies = Company.objects.filter(user_account=user_account)
    contractors = Contractor.objects.filter(user_account=user_account)

    invoice_stats = Invoice.invoice_stats
    currencies = Currency.objects.all()

    for invoice in Invoice.objects.filter(user_account=user_account):
        b = invoice.transactions.all().aggregate(Sum('sum_of_transactions')).get('sum_of_transactions__sum', None)
        if b:
            to_pay = round(invoice.invoice_sum - b, 2)
            if to_pay <= 0:
                to_pay = 0
            invoices.append([invoice, round((b / invoice.invoice_sum) * 100, 2), to_pay])
        else:
            invoices.append([invoice, 0, invoice.invoice_sum])

    context = {
        'invoices': invoices, 'companies': companies, 'contractors': contractors,
        'currencies': currencies, 'invoice_stats': invoice_stats
    }

    return render(request, 'invoice/invoice.html', context)


@login_required(login_url='/signin/')
def delete_invoice(request):
    Invoice.objects.get(
        uid=request.POST.get('uid'), user_account=User_Account.objects.get(owner=request.user)
    ).delete()

    return JsonResponse({}, status=200)


@login_required(login_url='/signin/')
def invoice_add(request):
    user_account = User_Account.objects.get(owner=request.user)

    products = Product.objects.filter(user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    contractors = Contractor.objects.filter(user_account=user_account)
    orders = Order.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()

    try:
        invoice_last = Invoice.objects.filter(user_account=user_account).latest('creation_date')
        invoice_number = int(invoice_last.invoice_name) + 1
    except ObjectDoesNotExist:
        invoice_number = 1

    if request.method == 'POST':

        form_invoice = InvoiceForm(user_account, request.POST)
        if form_invoice.is_valid():

            try:
                contractor = Contractor.objects.get(uid=request.POST.get('contractor'), user_account=user_account)
            except ValidationError:
                contractor = Contractor.objects.create(
                    contractor_name=request.POST.get('contractor'), user_account=user_account)

            form_invoice.instance.contractor = contractor
            form_invoice.instance.user_account = user_account

            invoice = form_invoice.save()

            quantities = request.POST.getlist('quantity')
            products = request.POST.getlist('product')
            prices = request.POST.getlist('price')

            instances = []

            for product, price, quantity in zip(products, prices, quantities):

                try:
                    product = Product.objects.get(uid=product, user_account=user_account)
                except ValidationError:
                    product = Product.objects.create(
                        user_account=user_account, product_name=product, product_price=price, currency=invoice.currency
                    )

                instances.append(
                    InvoiceItem(
                        user_account=user_account, product=product, invoice=invoice, quantity=int(quantity), price=float(price))
                )

            InvoiceItem.objects.bulk_create(instances)

            return redirect('invoice:invoice')
    else:
        form_invoice = InvoiceForm(user_account)

    context = {
        'currencies': currencies, 'companies': companies, 'contractors': contractors,
        'orders': orders, 'products': products, 'invoice_number': invoice_number, 'form_invoice': form_invoice
    }

    return render(request, 'invoice/invoice_add.html', context)


@login_required(login_url='/signin/')
def invoice_edit(request, inv_uid):
    user_account = User_Account.objects.get(owner=request.user)

    products = Product.objects.filter(user_account=user_account)
    invoice = Invoice.objects.get(uid=inv_uid, user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    orders = Order.objects.filter(user_account=user_account)
    contractors = Contractor.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()


    if request.method == 'POST':

        form_invoice = InvoiceForm(user_account, request.POST, instance=invoice)

        if form_invoice.is_valid():

            contractor_uid = request.POST.get('contractor')

            try:
                contractor = Contractor.objects.get(uid=contractor_uid, user_account=user_account)
            except ValidationError:
                contractor = Contractor.objects.create(
                    contractor_name=contractor_uid, user_account=user_account)

            form_invoice.instance.contractor = contractor
            invoice = form_invoice.save()


            items = request.POST.getlist('item')
            quantities = request.POST.getlist('quantity')  # quantity_new
            products = request.POST.getlist('product')  # select_item_new
            prices = request.POST.getlist('price')  # price_new

            quantities_new = request.POST.getlist('quantity_new')
            products_new = request.POST.getlist('select_item_new')
            prices_new = request.POST.getlist('price_new')

            for item, product, price, quantity in zip(items, products, prices, quantities):
                invoice_item = InvoiceItem.objects.filter(user_account=user_account, uid=item)

                try:
                    product = Product.objects.get(uid=product)
                except ValidationError:
                    product = Product.objects.create(user_account=user_account, product_name=product,
                                                     product_price=price, currency=invoice.currency)

                invoice_item.update(product=product, quantity=quantity, price=price)

            if quantities_new is not None and prices_new is not None and products_new is not None:
                for product, price, quantity in zip(products_new, prices_new, quantities_new):
                    try:
                        product = Product.objects.get(uid=product)
                    except ValidationError:
                        product = Product.objects.create(user_account=user_account, product_name=product,
                                                         product_price=price, currency=invoice.currency)

                    InvoiceItem.objects.create(user_account=user_account, product=product, invoice=invoice[0],
                                                              quantity=int(quantity), price=price)
            return redirect('invoice:invoice_edit', invoice.uid)
    else:
        form_invoice = InvoiceForm(user_account, instance=invoice)
    print(form_invoice.errors)
    context = {
        'orders': orders, 'currencies': currencies, 'companies': companies,
        'contractors': contractors, 'products': products, 'invoice': invoice, 'form_invoice': form_invoice,
               }

    return render(request, 'invoice/invoice_edit.html', context)


@login_required(login_url='/signin/')
def invoice_byOrder(request, ord_uid):
    user_account = User_Account.objects.get(owner=request.user)
    products = Product.objects.filter(user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    orders = Order.objects.filter(user_account=user_account)
    selected_order = Order.objects.get(user_account=user_account, uid=ord_uid)
    contractors = Contractor.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()

    try:
        invoice_last = Invoice.objects.filter(user_account=user_account).latest('creation_date')
        invoice_number = int(invoice_last.invoice_name) + 1
    except Exception:
        invoice_number = 1

    context = {'orders': orders, 'currencies': currencies, 'companies': companies, 'contractors': contractors,
               'products': products, 'invoice': invoice, 'selected_order': selected_order,
               'invoice_number': invoice_number}
    return render(request, 'invoice/invoice_byorder.html', context)


@login_required(login_url='/signin/')
def change_status(request):
    status = request.POST.get('status')
    invoice_uid = request.POST.get('invoice')

    Invoice.objects.filter(uid=invoice_uid).update(invoice_status=status)

    return JsonResponse({}, status=200)

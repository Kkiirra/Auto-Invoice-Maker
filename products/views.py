from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from company.models import Currency
from invoice.models import InvoiceItem
from orders.models import Order
from .models import Product, OrderItem
from customuser.models import User_Account
from invoice.models import Invoice
from django.contrib.auth.decorators import login_required


@login_required(login_url='/signin/')
def products(request):
    user_account = User_Account.objects.get(owner=request.user)

    products = Product.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()
    return render(request, 'products/products.html', {'currencies': currencies, 'products': products})


@login_required(login_url='/signin/')
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_cost = request.POST.get('product_cost')
        currency_name = request.POST.get('currency_name')

        user_account = User_Account.objects.get(owner=request.user)

        new_product = Product.objects.create(product_name=product_name, product_price=product_cost,
                                             currency=currency_name, user_account=user_account)
        return redirect('products:products')


@login_required(login_url='/signin/')
def delete_product(request):
    user_account = User_Account.objects.get(owner=request.user)
    prod_uid = request.POST.get('uid')

    if user_account:
        product = Product.objects.filter(user_account=user_account, uid=prod_uid)
        product.delete()
        return redirect('products:products')


@login_required(login_url='/signin/')
def product_edit(request, prod_uid):
    user_account = User_Account.objects.get(owner=request.user)
    currencies = Currency.objects.all()
    product = Product.objects.filter(user_account=user_account, uid=prod_uid)
    context = {'product': product[0], 'currencies': currencies}

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_cost = request.POST.get('product_cost')
        currency = request.POST.get('currency_name')

        product_price = product_cost.replace(',', '.')

        try:
            float(product_price)
        except ValueError:
            context['price_error'] = 'Please, enter the number value'
            return render(request, 'products/product_edit.html', context)

        product.update(product_name=product_name, product_price=product_price, currency=currency)

        return HttpResponseRedirect(f'/product/{prod_uid}/')
    else:
        return render(request, 'products/product_edit.html', context)


@login_required(login_url='/signin/')
def delete_item(request):
    user_account = User_Account.objects.get(owner=request.user)
    if user_account:
        uid = request.POST.get('id')
        order_uid = request.POST.get('order_uid')
        order_item = OrderItem.objects.get(uid=uid)
        order = Order.objects.get(user=user_account, uid=order_uid)
        new_total = float(order.order_sum) - float(order_item.price) * int(order_item.quantity)
        order.order_sum = new_total
        order.save()
        order_item.delete()
        return JsonResponse({}, status=200)


@login_required(login_url='/signin/')
def delete_invItem(request):
    user_account = User_Account.objects.get(owner=request.user)
    if user_account:
        uid = request.POST.get('id')
        invoice_uid = request.POST.get('invoice_uid')
        invoice_item = InvoiceItem.objects.get(uid=uid)
        invoice = Invoice.objects.get(user_account=user_account, uid=invoice_uid)
        new_total = float(invoice.invoice_sum) - float(invoice_item.price) * int(invoice_item.quantity)
        invoice.invoice_sum = new_total
        invoice.save()
        invoice_item.delete()
        return JsonResponse({}, status=200)



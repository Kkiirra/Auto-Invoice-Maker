from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from company.models import Currency
from .models import Product, OrderItem
from customuser.models import User_Account


def products(request):
    user_account = User_Account.objects.get(owner=request.user)

    products = Product.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()
    return render(request, 'products/products.html', {'currencies': currencies, 'products': products})


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_cost = request.POST.get('product_cost')
        currency_name = request.POST.get('currency_name')

        user_account = User_Account.objects.get(owner=request.user)

        new_product = Product.objects.create(product_name=product_name, product_price=product_cost,
                                             currency=currency_name, user_account=user_account)
        return redirect('products:products')


def delete_product(request):
    user_account = User_Account.objects.get(owner=request.user)
    prod_uid = request.POST.get('uid')

    if user_account:
        product = Product.objects.filter(user_account=user_account, uid=prod_uid)
        product.delete()
        return redirect('products:products')


def product_edit(request, prod_uid):
    user_account = User_Account.objects.get(owner=request.user)
    currencies = Currency.objects.all()

    product = Product.objects.filter(user_account=user_account, uid=prod_uid)

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_cost = request.POST.get('product_cost')
        currency = request.POST.get('currency_name')

        print(product_name, product_cost, currency)

        product.update(product_name=product_name, product_price=product_cost, currency=currency)

        return HttpResponseRedirect(f'/product/{prod_uid}/')
    else:
        return render(request, 'products/product_edit.html', {'product': product[0], 'currencies': currencies})


def delete_item(request):
    uid = request.POST.get('id')
    order_item = OrderItem.objects.get(uid=uid)
    order_item.delete()
    return JsonResponse({}, status=200)

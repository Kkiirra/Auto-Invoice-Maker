import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from customuser.models import User_Account
from .models import Order, Order_status
from company.models import Company, Currency
from contractors.models import Contractor
from dateutil.parser import parse
from django.core.exceptions import ValidationError
from products.models import Product, OrderItem


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
def order_edit(request, ord_uid):
    user_account = User_Account.objects.get(owner=request.user)

    products = Product.objects.filter(user_account=user_account)
    order = Order.objects.get(uid=ord_uid, user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    contractors = Contractor.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()

    context = {'order': order, 'currencies': currencies, 'companies': companies, 'contractors': contractors,
               'products': products}

    if request.method == 'POST':
        order_total = float(request.POST.get('order_total'))
        items = request.POST.getlist('item[]')
        currency = request.POST.get('currency_name')
        contractor_uid = request.POST.get('contractor_uid')
        order_number = request.POST.get('order_number')
        company_uid = request.POST.get('company_uid')
        order_date = parse(request.POST.get('datetimes'), dayfirst=True)

        quantities = request.POST.getlist('quantity[]')  # quantity_new
        products = request.POST.getlist('select_item')  # select_item_new
        prices = request.POST.getlist('price[]')  # price_new


        quantities_new = request.POST.getlist('quantity_new')
        products_new = request.POST.getlist('select_item_new')
        prices_new = request.POST.getlist('price_new')

        company = Company.objects.get(user_account=user_account, uid=company_uid)


        try:
            contractor = Contractor.objects.get(user_account=user_account, uid=contractor_uid)
        except ValidationError:
            contractor = Contractor.objects.create(user_account=user_account, contractor_name=contractor_uid)


        order = Order.objects.filter(user_account=user_account, uid=ord_uid)
        order.update(user_account=user_account, company=company, currency=currency,
                                         contractor=contractor, order_name=order_number, order_sum=order_total,
                                         order_date=order_date)

        for item, product, price, quantity in zip(items, products, prices, quantities):

            order_item = OrderItem.objects.filter(user_account=user_account, uid=item)

            try:
                product = Product.objects.filter(uid=product)
                product = product[0]
            except ValidationError:
                product = Product.objects.create(user_account=user_account, product_name=product,
                                                     product_price=price, currency=currency)
            order_item.update(product=product, quantity=quantity, price=price)

        if quantities_new is not None and prices_new is not None and products_new is not None:
            for product, price, quantity in zip(products_new, prices_new, quantities_new):
                try:
                    product = Product.objects.get(uid=product)
                except ValidationError:
                    product = Product.objects.create(user_account=user_account, product_name=product,
                                                     product_price=price, currency=currency)

                order_item = OrderItem.objects.create(user_account=user_account, product=product, order=order[0],
                                                      quantity=int(quantity), price=price)
        return HttpResponseRedirect(f'/orders/{ord_uid}/')

    else:
        return render(request, 'orders/order_edit.html', context)


@login_required(login_url='/signin/')
def order_add(request):

    user_account = User_Account.objects.get(owner=request.user)

    products = Product.objects.filter(user_account=user_account)
    companies = Company.objects.filter(user_account=user_account)
    contractors = Contractor.objects.filter(user_account=user_account)
    currencies = Currency.objects.all()

    try:
        order_last = Order.objects.filter(user_account=user_account).latest('creation_date')
        order_number = int(order_last.order_name) + 1
    except Exception:
        order_number = 1

    context = {'currencies': currencies, 'companies': companies, 'contractors': contractors,
               'products': products, 'order_number': order_number}

    if request.method == 'POST':

        order_total = float(request.POST.get('order_total'))
        order_status = request.POST.get('radio')
        currency = request.POST.get('currency_name')
        contractor_uid = request.POST.get('contractor_uid')
        company_uid = request.POST.get('company_uid')
        order_date = parse(request.POST.get('datetimes'), dayfirst=True)

        try:
            order_flag = Order.objects.get(user_account=user_account, order_name=order_number)
        except Exception:
            order_flag = False

        if order_flag:
            context['order_name_error'] = 'The same number is exist, please, enter the new'
        else:
            quantities = request.POST.getlist('quantity[]')
            products = request.POST.getlist('select_item')
            prices = request.POST.getlist('price[]')

            company = Company.objects.get(user_account=user_account, uid=company_uid)

            try:
                contractor = Contractor.objects.get(user_account=user_account, uid=contractor_uid)
            except ValidationError:
                contractor = Contractor.objects.create(user_account=user_account, contractor_name=contractor_uid)

            order_status = Order_status.objects.get(status=order_status)


            new_order = Order.objects.create(user_account=user_account, company=company, currency=currency,
                                             contractor=contractor, order_name=order_number, order_sum=order_total,
                                             order_status=order_status, order_date=order_date)


            for product, price, quantity in zip(products, prices, quantities):
                try:
                    product = Product.objects.get(uid=product)
                except ValidationError:
                    product = Product.objects.create(user_account=user_account, product_name=product,
                                                         product_price=price, currency=currency)

                order_item = OrderItem.objects.create(user_account=user_account, product=product, order=new_order,
                                                      quantity=int(quantity), price=price)
            return HttpResponseRedirect(f'/orders/')

    return render(request, 'orders/order_add.html', context)


@login_required(login_url='/signin/')
def change_status(request):
    status = request.POST.get('status')
    order_uid = request.POST.get('order')
    new_status = Order_status.objects.get(status=status)

    order = Order.objects.filter(uid=order_uid).update(order_status=new_status)


    return JsonResponse({}, status=200)


@login_required(login_url='/signin/')
def get_product(request):

    user_account = User_Account.objects.get(owner=request.user)

    try:
        uid_product = request.POST.get('product')
        product = Product.objects.get(uid=uid_product, user_account=user_account)
        return JsonResponse(data={'product_price': product.product_price}, status=200)

    except Exception:
        print('saggdsgasdg')


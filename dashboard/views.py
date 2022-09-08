from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from transactions.models import Transaction
from customuser.models import User_Account
from django.db.models import Sum, Max
from orders.models import Order
from datetime import datetime, timedelta
from dateutil.parser import parse


def daterange(date1, date2):
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    return [date1 + timedelta(days=x) for x in range((date2-date1).days + 1)]


def date_dashboard(request, date):

    try:
        date_range = date.split('-')
        date1 = parse(date_range[0], dayfirst=True)
        date2 = parse(date_range[1], dayfirst=True)
    except Exception:
        return HttpResponseRedirect('/bad_request/')

    date1 = date1.strftime('%Y-%m-%d')
    date2 = date2.strftime('%Y-%m-%d')

    date_range = [date1, date2]

    date_list = daterange(date_range[0], date_range[1])
    income_val_dict = dict()

    for i in date_list:
        income_val_dict[i.strftime('%m.%d')] = 0

    expenses_val_dict = income_val_dict.copy()
    order_val_dict = income_val_dict.copy()

    user_account = User_Account.objects.get(owner=request.user)

    orders = Order.objects.filter(user_account=user_account, order_date__range=date_range)

    total_order_value = orders.aggregate(Sum('order_sum'))['order_sum__sum']

    if total_order_value is None:
        total_order_value = 0


    income_transactions = Transaction.objects.filter(transaction_type='Income', user_account=user_account,
                                                     transaction_date__range=date_range).order_by('transaction_date')
    expenses_transactions = Transaction.objects.filter(transaction_type='Expenses', user_account=user_account,
                                                                                    transaction_date__range=date_range).order_by('transaction_date')
    for index in income_transactions:
        transaction_date = index.transaction_date.strftime('%m.%d')
        if income_val_dict[transaction_date]:
            income_val_dict[transaction_date] += index.sum_of_transactions
        else:
            income_val_dict[transaction_date] = index.sum_of_transactions

    for index in expenses_transactions:

        transaction_date = index.transaction_date.strftime('%m.%d')

        if expenses_val_dict[transaction_date]:
            expenses_val_dict[transaction_date] += index.sum_of_transactions
        else:
            expenses_val_dict[transaction_date] = index.sum_of_transactions

    for index in orders:
        order_date = index.order_date.strftime('%m.%d')
        if order_val_dict[order_date]:
            order_val_dict[order_date] += index.order_sum
        else:
            order_val_dict[order_date] = index.order_sum

    amount_of_income = income_transactions.aggregate(Sum('sum_of_transactions'))
    amount_of_expenses = expenses_transactions.aggregate(Sum('sum_of_transactions'))

    try:
        average_order_value = round(total_order_value / orders.count(), 2)
    except (TypeError, ZeroDivisionError):
        average_order_value = 0

    try:
        amount_of_income = round(amount_of_income['sum_of_transactions__sum'], 2)
    except TypeError:
        amount_of_income = 0

    try:
        amount_of_expenses = round(amount_of_expenses['sum_of_transactions__sum'], 2)
    except TypeError:
        amount_of_expenses = 0

    balance = amount_of_income - amount_of_expenses

    if amount_of_income != 0:
        balance_procent = round((balance / amount_of_income) * 100, 2)
    else:
        balance_procent = 0

    max1 = max(income_val_dict.values())
    max2 = max(expenses_val_dict.values())

    if max1 >= max2:
        max_transaction = max1
    else:
        max_transaction = max2

    if max_transaction is None:
        max_transaction = 0

    max_order = max(order_val_dict.values())

    context = {
        'income_transactions': income_val_dict,
        'expenses_transactions': expenses_val_dict,
        'total_order_value': total_order_value,
        'amount_of_income': amount_of_income,
        'average_order_value': average_order_value,
        'order_val_dict': order_val_dict,
        'amount_of_expenses': amount_of_expenses,
        'max_transaction': max_transaction,
        'max_order': max_order,
        'gap': abs(balance),
        'gap_procent': round(abs(balance_procent), 2)
    }
    if request.method == 'GET':
        return render(request, 'dashboard/dashboard.html', context=context)
    else:
        return JsonResponse({'income_transactionss': income_val_dict, 'expenses_transactionss': expenses_val_dict},
                            status=200)


def dashboard(request):
    if request.user.is_authenticated:
        date_range = ['2022-08-01', '2022-09-07']

        date_list = daterange(date_range[0], date_range[1])
        income_val_dict = dict()

        for i in date_list:
            income_val_dict[i.strftime('%m.%d')] = 0

        expenses_val_dict = income_val_dict.copy()
        order_val_dict = income_val_dict.copy()

        user_account = User_Account.objects.get(owner=request.user)

        orders = Order.objects.filter(user_account=user_account)

        total_order_value = orders.aggregate(Sum('order_sum'))['order_sum__sum']

        if total_order_value is None:
            total_order_value = 0


        income_transactions = Transaction.objects.filter(transaction_type='Income', user_account=user_account,
                                                         transaction_date__range=date_range).order_by('transaction_date')
        expenses_transactions = Transaction.objects.filter(transaction_type='Expenses', user_account=user_account,
                                                                                        transaction_date__range=date_range).order_by('transaction_date')

        for index in income_transactions:
            transaction_date = index.transaction_date.strftime('%m.%d')

            if income_val_dict[transaction_date]:
                income_val_dict[transaction_date] += index.sum_of_transactions
            else:
                income_val_dict[transaction_date] = index.sum_of_transactions

        for index in expenses_transactions:

            transaction_date = index.transaction_date.strftime('%m.%d')

            if expenses_val_dict[transaction_date]:
                expenses_val_dict[transaction_date] += index.sum_of_transactions
            else:
                expenses_val_dict[transaction_date] = index.sum_of_transactions

        for index in orders:
            order_date = index.order_date.strftime('%m.%d')
            if order_val_dict[order_date]:
                order_val_dict[order_date] += index.order_sum
            else:
                order_val_dict[order_date] = index.order_sum

        amount_of_income = income_transactions.aggregate(Sum('sum_of_transactions'))
        amount_of_expenses = expenses_transactions.aggregate(Sum('sum_of_transactions'))

        try:
            average_order_value = round(total_order_value / orders.count(), 2)
        except (TypeError, ZeroDivisionError):
            average_order_value = 0

        try:
            amount_of_income = round(amount_of_income['sum_of_transactions__sum'], 2)
        except TypeError:
            amount_of_income = 0

        try:
            amount_of_expenses = round(amount_of_expenses['sum_of_transactions__sum'], 2)
        except TypeError:
            amount_of_expenses = 0

        matches = income_val_dict | expenses_val_dict
        balance = amount_of_income - amount_of_expenses

        if amount_of_income != 0:
            balance_procent = round((balance / amount_of_income) * 100, 2)
        else:
            balance_procent = 0

        max_transaction = max(matches.values())

        if max_transaction is None:
            max_transaction = 0

        max_order = max(order_val_dict.values())

        context = {
            'income_transactions': income_val_dict,
            'expenses_transactions': expenses_val_dict,
            'total_order_value': total_order_value,
            'amount_of_income': amount_of_income,
            'average_order_value': average_order_value,
            'order_val_dict': order_val_dict,
            'amount_of_expenses': amount_of_expenses,
            'max_transaction': max_transaction,
            'max_order': max_order,
            'gap': abs(balance),
            'gap_procent': round(abs(balance_procent), 2)
        }
        if request.method == 'GET':
            return render(request, 'dashboard/dashboard.html', context=context)
        else:
            return JsonResponse({'income_transactionss': income_val_dict, 'expenses_transactionss': expenses_val_dict},
                                status=200)
    else:
        return HttpResponseRedirect('/signin/')

#

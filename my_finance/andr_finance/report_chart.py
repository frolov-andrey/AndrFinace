import json
from datetime import timedelta, date
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncDate

from .models import Transaction, Account


def get_chart_line(filters, transactions_by_date_plus, transactions_by_date_minus):
    balance = Decimal(0)

    accounts = Account.objects.all()
    for account in accounts:
        if account.start_balance > 0:
            balance = balance + account.start_balance

    datas_plus = {}
    for data_list in list(transactions_by_date_plus):
        datas_plus[data_list['transaction_date']] = data_list['total_expense']

    datas_minus = {}
    for data_list in list(transactions_by_date_minus):
        datas_minus[data_list['transaction_date']] = data_list['total_expense']

    start_date = date(2024, 4, 1)
    end_date = date(2024, 4, 30)
    current_date = start_date

    datas_chart = []
    while current_date <= end_date:
        current_date += timedelta(days=1)
        if current_date in datas_minus or current_date in datas_plus:
            sum_day = Decimal(0)

            if current_date in datas_plus:
                sum_day = sum_day + datas_plus[current_date]

            if current_date in datas_minus:
                sum_day = sum_day - datas_minus[current_date]

            balance = balance + sum_day
            datas_chart.append({
                'x': current_date.strftime('%d.%m.%Y'),
                'y': str(balance),
            })

    data_chart_str = json.dumps(datas_chart, indent=4)

    return data_chart_str


def get_chart_str(transactions_by_date, type_transaction):
    datas_chart = []
    for transaction_by_date in transactions_by_date:
        sum_day = Decimal(0)
        if type_transaction == Transaction.PLUS:
            sum_day = transaction_by_date['total_expense']
        elif type_transaction == Transaction.MINUS:
            sum_day = sum_day - transaction_by_date['total_expense']

        datas_chart.append({
            'x': transaction_by_date['transaction_date'].strftime('%d.%m.%Y'),
            'y': str(sum_day),
        })
    return  datas_chart


def get_chart_bar(filters, type_transaction):
    transactions_by_date = []
    if type_transaction == Transaction.PLUS:
        transactions_by_date = Transaction.objects.filter(type_transaction='plus').annotate(
            transaction_date=TruncDate('date_add')
        ).values('transaction_date').annotate(
            total_expense=Sum('amount')
        ).order_by('transaction_date')
    elif type_transaction == Transaction.MINUS:
        transactions_by_date = Transaction.objects.filter(type_transaction='minus').annotate(
            transaction_date=TruncDate('date_add')
        ).values('transaction_date').annotate(
            total_expense=Sum('amount')
        ).order_by('transaction_date')

    return transactions_by_date

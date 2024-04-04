import json
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_DOWN
from operator import itemgetter

from django.db.models import Sum, Q
from django.db.models.functions import TruncDate

from .models import Transaction, Account, Category
from .report_table import get_sum_transaction


def get_chart_line(filters, transactions_by_date_plus, transactions_by_date_minus, min_date, max_date):
    balance = Decimal(0)

    if 'account_id' in filters:
        accounts = Account.objects.filter(pk=filters['account_id'])
        if accounts.exists():
            balance = balance + accounts.get().start_balance
    else:
        accounts = Account.objects.all()
        for account in accounts:
            if account.start_balance > 0:
                balance = balance + account.start_balance

    if 'date_start' in filters:
        transactions_for_start_balance = Transaction.objects.filter(date_add__lt=filters["date_start"])
        sum_transaction = get_sum_transaction(transactions_for_start_balance, filters)
        balance = balance + sum_transaction

    datas_plus = {}
    for data_list in list(transactions_by_date_plus):
        datas_plus[data_list['transaction_date']] = data_list['total_expense']

    datas_minus = {}
    for data_list in list(transactions_by_date_minus):
        datas_minus[data_list['transaction_date']] = data_list['total_expense']

    current_date = min_date
    datas_list = []
    while current_date <= max_date:
        if current_date in datas_minus or current_date in datas_plus:
            sum_day = Decimal(0)
            if current_date in datas_plus:
                sum_day = sum_day + datas_plus[current_date]
            if current_date in datas_minus:
                sum_day = sum_day - datas_minus[current_date]

            balance = balance + sum_day
            datas_list.append(float(balance.quantize(Decimal("1.00"), ROUND_HALF_DOWN)))
        else:
            datas_list.append(float(balance.quantize(Decimal("1.00"), ROUND_HALF_DOWN)))

        current_date += timedelta(days=1)

    data_chart_str = json.dumps(datas_list, indent=4)

    return data_chart_str


def get_chart_str(filters, transactions_by_date, type_transaction, min_date, max_date):
    datas_dict = {}
    for data_list in list(transactions_by_date):
        datas_dict[data_list['transaction_date']] = data_list['total_expense']

    current_date = min_date
    datas_list = []
    while current_date <= max_date:
        if current_date in datas_dict:
            sum_day = Decimal(0)
            if type_transaction == Transaction.PLUS:
                sum_day = datas_dict[current_date]
            elif type_transaction == Transaction.MINUS:
                sum_day = sum_day - datas_dict[current_date]
            elif 'account_id' in filters and type_transaction == Transaction.TRANSFER:
                sum_day = sum_day - datas_dict[current_date]

            datas_list.append(float(sum_day.quantize(Decimal("1.00"), ROUND_HALF_DOWN)))
        else:
            datas_list.append(0)

        current_date += timedelta(days=1)

    datas_chart_str = json.dumps(datas_list, indent=4)

    return datas_chart_str


def get_chart_bar(filters, transactions, type_transaction):
    if 'account_id' in filters:
        if type_transaction == Transaction.PLUS:
            transactions = transactions.filter(
                (
                        Q(account_id=filters['account_id']) & Q(type_transaction=Transaction.PLUS)
                )
                |
                (
                        Q(account_recipient_id=filters['account_id']) & Q(type_transaction=Transaction.TRANSFER)
                )
            )
        elif type_transaction == Transaction.MINUS:
            transactions = transactions.filter(
                (
                        Q(account_id=filters['account_id']) & Q(type_transaction=Transaction.MINUS)
                )
                |
                (
                        Q(account_id=filters['account_id']) & Q(type_transaction=Transaction.TRANSFER)
                )
            )
    else:
        transactions = transactions.filter(type_transaction=type_transaction)

    transactions_by_date = transactions.annotate(
        transaction_date=TruncDate('date_add')
    ).values('transaction_date').annotate(
        total_expense=Sum('amount')
    ).order_by('transaction_date')

    return transactions_by_date


def get_min_max_date(filters, transactions_by_date_plus, transactions_by_date_minus):
    all_set = set()
    for transaction_by_date_plus in transactions_by_date_plus:
        all_set.add(transaction_by_date_plus['transaction_date'])
    for transaction_by_date_minus in transactions_by_date_minus:
        all_set.add(transaction_by_date_minus['transaction_date'])

    if len(all_set) > 0:
        min_date = min(all_set)
        max_date = max(all_set)
    else:
        if 'date_start' in filters:
            min_date = filters['date_start'].date()
        if 'date_end' in filters:
            max_date = filters['date_end'].date()

    if 'date_start' in filters:
        if min_date > filters['date_start'].date():
            min_date = filters['date_start'].date()

    if 'date_end' in filters:
        if max_date < filters['date_end'].date():
            max_date = filters['date_end'].date()

    return min_date, max_date


def get_labels(min_date, max_date):
    current_date = min_date
    datas_list = []
    while current_date < max_date:
        datas_list.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)

    datas_label_str = json.dumps(datas_list, indent=4)

    return datas_label_str


def get_chart_bar_category(transactions):
    chart = []
    categories = Category.objects.all()
    for category in categories:
        transactions_category = transactions.filter(category_id=category.id).all()
        if transactions_category.exists():
            chart.append({
                'category_name': category.name,
                'amount': transactions_category.aggregate(Sum('amount'))['amount__sum'].quantize(Decimal("1.00"),
                                                                                                 ROUND_HALF_DOWN),
            })

    chart = sorted(chart, key=itemgetter('amount'), reverse=True)

    return chart

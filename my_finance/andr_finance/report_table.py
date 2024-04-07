from datetime import datetime, timedelta
from decimal import Decimal
from operator import itemgetter

from django.db.models import Sum, Q

from .models import Transaction, Account, Category


def get_filter_transaction(request):
    filters = {}

    sort_field = request.GET.get('sort_field')
    if sort_field == 'balance':
        filters['sort_field'] = sort_field

    for field in Transaction._meta.fields:
        if field.name == sort_field:
            filters['sort_field'] = sort_field
            break

    sort_order = request.GET.get('sort_order')
    if sort_order == 'asc' or sort_order == 'desc':
        filters['sort_order'] = sort_order

    filter_account = request.GET.get('filter_account')
    if filter_account is not None and filter_account != '0':
        filter_account = int(filter_account)
        if Account.objects.filter(pk=filter_account).count() > 0:
            filters['account_id'] = filter_account

    filter_category = request.GET.get('filter_category')
    if filter_category is not None and filter_category != '0':
        filter_category = int(filter_category)
        if Category.objects.filter(pk=filter_category).count() > 0:
            filters['category_id'] = filter_category

    filter_type_transaction = request.GET.get('filter_type_transaction')
    if (filter_type_transaction == Transaction.MINUS
            or filter_type_transaction == Transaction.PLUS
            or filter_type_transaction == Transaction.TRANSFER):
        filters['type_transaction'] = filter_type_transaction

    filter_group_category = request.GET.get('filter_group_category')
    if filter_group_category == 'on':
        filters['filter_group_category'] = 'on'

    filter_date_start = request.GET.get('filter_date_start')
    try:
        filter_date_start = datetime.strptime(filter_date_start, '%d.%m.%Y')
    except:
        filter_date_start = ''
    if filter_date_start != '':
        filters['date_start'] = filter_date_start

    filter_date_end = request.GET.get('filter_date_end')
    try:
        filter_date_end = datetime.strptime(filter_date_end, '%d.%m.%Y')
    except:
        filter_date_end = ''
    if filter_date_end != '':
        filter_date_end = filter_date_end + timedelta(days=1)
        filters['date_end'] = filter_date_end

    return filters


def get_sum_transaction_type(transaction_type, transactions, account_id=0, main_account=True):
    transactions = transactions.filter(type_transaction=transaction_type)
    if account_id != 0:
        if main_account:
            transactions = transactions.filter(account_id=account_id)
        else:
            transactions = transactions.filter(account_recipient_id=account_id)

    transaction_sum = transactions.aggregate(Sum('amount'))
    if transaction_sum['amount__sum'] is not None:
        total_sum = Decimal(transaction_sum['amount__sum'])
    else:
        total_sum = Decimal(0)

    return total_sum


def get_sum_transaction(transactions, filters):
    if 'account_id' in filters:
        account_id = filters['account_id']
    else:
        account_id = 0

    total_plus = get_sum_transaction_type(Transaction.PLUS, transactions, account_id, main_account=True)
    total_mimus = get_sum_transaction_type(Transaction.MINUS, transactions, account_id, main_account=True)
    total_transfer = get_sum_transaction_type(Transaction.TRANSFER, transactions, account_id, main_account=True)
    total_transfer_recipient = get_sum_transaction_type(Transaction.TRANSFER, transactions, account_id,
                                                        main_account=False)

    # print('total_plus', total_plus)
    # print('total_mimus', total_mimus)
    # print('total_transfer', total_transfer)
    # print('total_transfer_recipient', total_transfer_recipient)

    balance = (
            total_plus
            - total_mimus
            - total_transfer
            + total_transfer_recipient
    )

    return balance


def get_transaction(filters, request):
    transactions = Transaction.objects.filter(user=request.user)

    if len(filters) == 0:
        return transactions.all().order_by('date_add')

    if 'account_id' in filters:
        transactions = transactions.filter(
            Q(account=filters['account_id']) | Q(account_recipient=filters['account_id']))

    if 'category_id' in filters:
        transactions = transactions.filter(category=filters['category_id'])

    if 'type_transaction' in filters:
        transactions = transactions.filter(type_transaction=filters['type_transaction'])

    if 'date_start' in filters:
        transactions = transactions.filter(date_add__gte=filters['date_start'])

    if 'date_end' in filters:
        transactions = transactions.filter(date_add__lt=filters['date_end'])

    if 'sort_field' in filters:
        sort_field = filters['sort_field']
        if sort_field == 'category':
            sort_field = 'category__name'
        elif sort_field == 'account':
            sort_field = 'account__name'
    else:
        sort_field = 'date_add'

    transactions = transactions.order_by(get_sort_order(filters) + sort_field, 'id')

    return transactions


def get_sort_order(filters):
    if 'sort_order' in filters:
        if filters['sort_order'] == 'asc':
            sort_order = '-'
        elif filters['sort_order'] == 'desc':
            sort_order = ''
        else:
            sort_order = ''
    else:
        sort_order = '-'

    return sort_order


def get_balances(transactions, filters, request):
    balances = {}
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
        transactions_for_start_balance = Transaction.objects.filter(user=request.user).filter(
            date_add__lt=filters["date_start"]
        )
        sum_transaction = get_sum_transaction(transactions_for_start_balance, filters)
        balance = balance + sum_transaction

    transactions_balance = transactions.order_by('date_add', 'id')
    for transaction_balance in transactions_balance:
        if transaction_balance.type_transaction == Transaction.MINUS:
            balance = balance - transaction_balance.amount
            balances[transaction_balance.id] = balance
        elif transaction_balance.type_transaction == Transaction.PLUS:
            balance = balance + transaction_balance.amount
            balances[transaction_balance.id] = balance
        elif transaction_balance.type_transaction == Transaction.TRANSFER:
            if 'account_id' in filters:
                if filters['account_id'] == transaction_balance.account_id:
                    balance = balance - transaction_balance.amount
                    balances[transaction_balance.id] = balance
                elif filters['account_id'] == transaction_balance.account_recipient_id:
                    balance = balance + transaction_balance.amount
                    balances[transaction_balance.id] = balance
                else:
                    raise Exception("Такого не может быть!: " +
                                    "filters['account_id'] == transaction_balance.account_id, " +
                                    "filters['account_id'] == transaction_balance.account_recipient_id,  ")
            else:
                balances[transaction_balance.id] = balance

    return balances


def get_transactions_group(filters, request):
    result = []
    transactions = get_transaction(filters, request)

    if 'filter_group_category' in filters:
        if filters['filter_group_category'] == 'on':
            transactions_group = transactions.values('category').annotate(total=Sum('amount')).order_by('category__name')
            for transaction_group in transactions_group:
                transactions_category = transactions.filter(category=transaction_group['category'])
                if transaction_group['category'] is not None:
                    category = Category.objects.get(pk=transaction_group['category'])
                    category_name = category.name
                    category_icon_folder = category.icon_folder
                    category_icon_file = category.icon_file
                else:
                    category_name = '---нет---'
                    category_icon_folder = ''
                    category_icon_file = ''

                result.append({
                    'category_id': str(transaction_group['category']),
                    'category_name': category_name,
                    'category_icon_folder': category_icon_folder,
                    'category_icon_file': category_icon_file,
                    'total': transaction_group['total'],
                    'transactions': transactions_category,
                })

            if 'sort_field' in filters:
                sort_field = filters['sort_field']
                if sort_field == 'category':
                    sort_field = 'category_name'
                elif sort_field == 'amount':
                    sort_field = 'total'
                else:
                    sort_field = 'category_name'
            else:
                sort_field = 'category_name'

            if 'sort_order' in filters:
                if filters['sort_order'] == 'asc':
                    reverse = True
                elif filters['sort_order'] == 'desc':
                    reverse = False
                else:
                    reverse = False
            else:
                reverse = True

            result = sorted(result, key=itemgetter(sort_field), reverse=reverse)

    return result

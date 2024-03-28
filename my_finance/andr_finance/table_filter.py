from decimal import Decimal

from django.db.models import Sum, Q

from .models import Transaction, Account, Category


def get_filter_transaction(request):
    filters = {}

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


def get_balance(transactions, filters):
    if 'account_id' in filters:
        account_id = filters['account_id']
    else:
        account_id = 0

    total_plus = get_sum_transaction_type(Transaction.PLUS, transactions, account_id, main_account=True)
    total_mimus = get_sum_transaction_type(Transaction.MINUS, transactions, account_id, main_account=True)
    total_transfer = get_sum_transaction_type(Transaction.TRANSFER, transactions, account_id, main_account=True)
    total_transfer_recipient = get_sum_transaction_type(Transaction.TRANSFER, transactions, account_id, main_account=False)

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


def get_transaction(filters):
    transactions = Transaction.objects

    if len(filters) == 0:
        return transactions.all()

    if 'account_id' in filters:
        transactions = transactions.filter(
            Q(account=filters['account_id']) | Q(account_recipient=filters['account_id']))

    if 'category_id' in filters:
        transactions = transactions.filter(category=filters['category_id'])

    if 'type_transaction' in filters:
        transactions = transactions.filter(type_transaction=filters['type_transaction'])

    transactions = transactions.order_by('date_added')

    return transactions

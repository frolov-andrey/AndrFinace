import json
from datetime import datetime
from decimal import Decimal

from django.conf import settings

from andr_finance.models import Account, Transaction, Category


def load_demo_data():
    path_folder_demo = str(settings.BASE_DIR) + '/andr_finance/' + str(settings.STATIC_URL) +'andr_finance/demo/'

    with open(path_folder_demo + 'accounts.json', 'rt', encoding='utf-8') as file_accounts:
        data_accounts = json.load(file_accounts)

    with open(path_folder_demo + 'categories.json', 'rt',
              encoding='utf-8') as file_categories:
        data_categories = json.load(file_categories)

    with open(path_folder_demo + 'transactions.json', 'rt',
              encoding='utf-8') as file_transactions:
        data_transactions = json.load(file_transactions)

    # print(data_accounts)
    transactions = Transaction.objects.all()
    transactions.delete()

    accounts = Account.objects.all()
    accounts.delete()

    categories = Category.objects.all()
    categories.delete()

    for data_account in data_accounts:
        Account.objects.create(
            name=data_account['name'],
            start_balance=data_account['start_balance'],
            icon_folder=data_account['icon_folder'],
            icon_file=data_account['icon_file']
        )

    for data_category in data_categories:
        Category.objects.create(
            name=data_category['name'],
            icon_folder=data_category['icon_folder'],
            icon_file=data_category['icon_file']
        )

    for data_transaction in data_transactions:
        account = Account.objects.filter(name=data_transaction['account_name'])
        if account.exists():
            account_id = account.get().id
        else:
            account_id = None

        account_recipient = Account.objects.filter(name=data_transaction['account_recipient_name'])
        if account_recipient.exists():
            account_recipient_id = account_recipient.get().id
        else:
            account_recipient_id = None

        category = Category.objects.filter(name=data_transaction['category_name'])
        if category.exists():
            category_id = category.get().id
        else:
            category_id = None

        current_date = datetime.now()
        date_add = datetime.strptime(data_transaction['date_add'], "%d.%m.%Y %H:%M")
        date_add = date_add.replace(month=current_date.month)

        Transaction.objects.create(
            account_id=account_id,
            account_recipient_id=account_recipient_id,
            type_transaction=data_transaction['type_transaction'],
            amount=Decimal(data_transaction['amount']),
            category_id=category_id,
            date_add=date_add,
            title=data_transaction['title']
        )

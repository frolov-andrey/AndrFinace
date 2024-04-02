import os
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .demo import load_demo_data
from .forms import CategoryForm, AccountForm, TransactionFormMinusPlus, TransactionFormTransfer
from .models import Account, Category, Transaction
from .report_chart import get_chart_line, get_chart_bar, get_chart_str
from .report_table import get_filter_transaction, get_transaction, get_transactions_group, get_balances, \
    get_sum_transaction

folders = [
    {'name': 'finance', 'name_rus': 'Финансы'},
    {'name': 'people', 'name_rus': 'Люди'},
    {'name': 'foot', 'name_rus': 'Еда'},
    {'name': 'animals', 'name_rus': 'Животные'},
    {'name': 'different', 'name_rus': 'Разное'},
]
images_path = str(settings.STATIC_URL) + 'andr_finance/item_images/'
icon_default = images_path + 'default/default_icon.png'


def page_not_found(request):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def get_images(images_path, catalog=None):
    images = []
    is_find_image = False
    for folder in folders:
        images_files = os.listdir(str(settings.BASE_DIR) + '/andr_finance' + images_path + folder['name'])
        if catalog is not None and catalog.icon_folder == folder['name']:
            active = 'active'
            show = 'show'
            aria_selected = True

            is_find_image = True
        else:
            active = ''
            show = ''
            aria_selected = False

        images.append({
            'folder': folder['name'],
            'name_rus': folder['name_rus'],
            'images': images_files,
            'aria_selected': aria_selected,
            'active': active,
            'show': show,
        })

    if is_find_image == False:
        images[0]['active'] = 'active'
        images[0]['show'] = 'show'
        images[0]['aria_selected'] = True

    return images


def index(request):
    context = {
        'select_menu': 'index'
    }
    return render(request, 'andr_finance/index.html', context)


# --- Category ---
def categories(request):
    categories = Category.objects.order_by('name')
    context = {
        'categories': categories,
        'select_menu': 'categories',
        'icon_default': icon_default,
    }
    return render(request, 'andr_finance/categories.html', context)


def category_add(request):
    images = get_images(images_path)

    if request.method != 'POST':
        form = CategoryForm
    else:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.icon_folder = form.data['icon_folder']
            category.icon_file = form.data['icon_file']
            category.save()
            return redirect('andr_finance:categories')

    context = {
        'form': form,
        'select_menu': 'categories',
        'images': images,
        'images_path': images_path,
        'image_default_folder': 'default',
        'image_default_file': 'default_icon.png',
    }
    return render(request, 'andr_finance/category_add.html', context)


def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)
    images = get_images(images_path, category)

    if request.method != 'POST':
        form = CategoryForm(instance=category)
    else:
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.icon_folder = form.data['icon_folder']
            category.icon_file = form.data['icon_file']
            category.save()
            return redirect('andr_finance:categories')

    context = {
        'category': category,
        'form': form,
        'select_menu': 'categories',
        'images': images,
        'images_path': images_path,
        'image_default_folder': 'default',
        'image_default_file': 'default_icon.png',
        'icon_file': category.icon_file,
        'icon_folder': category.icon_folder,
    }
    return render(request, 'andr_finance/category_edit.html', context)


def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'The category has been deleted successfully: ' + category.name)
        return redirect('andr_finance:categories')


# --- Account ---
def accounts(request):
    accounts = Account.objects.order_by('name')
    context_accounts = []
    for account in accounts:
        if account.start_balance:
            balance = account.start_balance
        else:
            balance = Decimal(0)

        transactions = get_transaction({'account_id': account.id})
        sum_transaction = get_sum_transaction(transactions, {'account_id': account.id})
        balance = balance + sum_transaction
        o_account = {'account': account, 'balance': balance}
        context_accounts.append(o_account)

    context = {
        'context_accounts': context_accounts,
        'select_menu': 'accounts',
        'icon_default': icon_default,
    }

    return render(request, 'andr_finance/accounts.html', context)


def account_add(request):
    images = get_images(images_path)

    if request.method != 'POST':
        form = AccountForm
    else:
        form = AccountForm(data=request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.icon_folder = form.data['icon_folder']
            account.icon_file = form.data['icon_file']
            account.save()
            return redirect('andr_finance:accounts')

    context = {
        'form': form,
        'select_menu': 'accounts',
        'images': images,
        'images_path': images_path,
        'image_default_folder': 'default',
        'image_default_file': 'default_icon.png',
    }
    return render(request, 'andr_finance/account_add.html', context)


def account_edit(request, account_id):
    images = get_images(images_path)
    account = Account.objects.get(id=account_id)

    if request.method != 'POST':
        form = AccountForm(instance=account)
    else:
        form = AccountForm(instance=account, data=request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.icon_folder = form.data['icon_folder']
            account.icon_file = form.data['icon_file']
            account.save()
            return redirect('andr_finance:accounts')

    context = {
        'account': account,
        'form': form,
        'select_menu': 'accounts',
        'images': images,
        'images_path': images_path,
        'image_default_folder': 'default',
        'image_default_file': 'default_icon.png',
        'icon_file': account.icon_file,
        'icon_folder': account.icon_folder,
    }
    return render(request, 'andr_finance/account_edit.html', context)


def account_delete(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'The currency has been deleted successfully: ' + account.name)
        return redirect('andr_finance:accounts')


# --- Transaction ---
def transactions(request):
    filters = get_filter_transaction(request)

    if 'filter_group_category' in filters:
        group_by = filters['filter_group_category']
        transactions_group = get_transactions_group(filters)
    else:
        group_by = ''
        transactions_group = []

    transactions = get_transaction(filters)
    balances = get_balances(transactions, filters)

    type_transactions = [
        {'code': Transaction.MINUS, 'name': Transaction.TYPE_TRANSACTION[0][1]},
        {'code': Transaction.PLUS, 'name': Transaction.TYPE_TRANSACTION[1][1]},
        {'code': Transaction.TRANSFER, 'name': Transaction.TYPE_TRANSACTION[2][1]},
    ]

    send_filter_date_start = request.GET.get('filter_date_start')
    if send_filter_date_start is None:
        send_filter_date_start = ''

    send_filter_date_end = request.GET.get('filter_date_end')
    if send_filter_date_end is None:
        send_filter_date_end = ''

    if 'sort_field' in filters:
        sort_field = filters['sort_field']
    else:
        sort_field = 'date_add'

    if 'sort_order' in filters:
        sort_order = filters['sort_order']
    else:
        sort_order = 'asc'  # asc, desc

    context = {
        'sort_field': sort_field,
        'sort_order': sort_order,
        'group_by': group_by,
        'transactions': transactions,
        'balances': balances,
        'transactions_group': transactions_group,
        'accounts': Account.objects.order_by('name'),
        'categories': Category.objects.order_by('name'),
        'type_transactions': type_transactions,
        'select_menu': 'transactions',
        'icon_default': icon_default,

        'filter_account': request.GET.get('filter_account'),
        'filter_category': request.GET.get('filter_category'),
        'filter_type_transaction': request.GET.get('filter_type_transaction'),
        'filter_date_start': send_filter_date_start,
        'filter_date_end': send_filter_date_end,
        'filter_group_category': request.GET.get('filter_group_category'),

    }

    return render(request, 'andr_finance/transactions.html', context)


def transaction_add(request, type_transaction):
    if request.method != 'POST':
        if type_transaction == Transaction.MINUS or type_transaction == Transaction.PLUS:
            form = TransactionFormMinusPlus()
        elif type_transaction == type_transaction == Transaction.TRANSFER:
            form = TransactionFormTransfer()
        else:
            return page_not_found(request)
    else:
        if type_transaction == Transaction.MINUS or type_transaction == Transaction.PLUS:
            form = TransactionFormMinusPlus(data=request.POST)
        elif type_transaction == type_transaction == Transaction.TRANSFER:
            form = TransactionFormTransfer(data=request.POST)
        else:
            return page_not_found(request)

        if form.is_valid():
            transaction = form.save(commit=False)

            if type_transaction == Transaction.MINUS:
                transaction.type_transaction = Transaction.MINUS
                transaction.account_recipient = None
            elif type_transaction == Transaction.PLUS:
                transaction.type_transaction = Transaction.PLUS
                transaction.account_recipient = None
            elif type_transaction == Transaction.TRANSFER:
                transaction.type_transaction = Transaction.TRANSFER

            transaction.save()

            return redirect('andr_finance:transactions')

    context = {
        'form': form,
        'select_menu': 'transactions',
        'type_transaction': type_transaction,
    }
    return render(request, 'andr_finance/transaction_add.html', context)


def transaction_edit(request, type_transaction, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method != 'POST':
        if type_transaction == Transaction.MINUS or type_transaction == Transaction.PLUS:
            form = TransactionFormMinusPlus(instance=transaction)
        elif type_transaction == type_transaction == Transaction.TRANSFER:
            form = TransactionFormTransfer(instance=transaction)
        else:
            return page_not_found(request)
    else:
        if type_transaction == Transaction.MINUS or type_transaction == Transaction.PLUS:
            form = TransactionFormMinusPlus(instance=transaction, data=request.POST)
        elif type_transaction == type_transaction == Transaction.TRANSFER:
            form = TransactionFormTransfer(instance=transaction, data=request.POST)
        else:
            return page_not_found(request)
        if form.is_valid():
            transaction = form.save(commit=False)

            if type_transaction == Transaction.MINUS:
                transaction.type_transaction = Transaction.MINUS
                transaction.account_recipient = None
            elif type_transaction == Transaction.PLUS:
                transaction.type_transaction = Transaction.PLUS
                transaction.account_recipient = None
            elif type_transaction == Transaction.TRANSFER:
                transaction.type_transaction = Transaction.TRANSFER

            transaction.save()

            return redirect('andr_finance:transactions')

    context = {
        'transaction': transaction,
        'form': form,
        'select_menu': 'transactions',
        'type_transaction': type_transaction,
    }
    return render(request, 'andr_finance/transaction_edit.html', context)


def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == 'GET':
        transaction.delete()
        messages.success(
            request,
            'The transaction has been deleted successfully: ' +
            transaction.date_add.strftime('%d.%m.%Y %H:%M')
        )
        return redirect('andr_finance:transactions')


def reports(request):
    filters = {}

    transactions_by_date_plus = get_chart_bar(filters, 'plus')
    chart_bar_plus = get_chart_str(transactions_by_date_plus, 'plus')

    transactions_by_date_minus = get_chart_bar(filters, 'minus')
    chart_bar_minus = get_chart_str(transactions_by_date_minus, 'minus')

    chart_line = get_chart_line(filters, transactions_by_date_plus, transactions_by_date_minus)

    send_filter_date_start = request.GET.get('filter_date_start')
    if send_filter_date_start is None:
        send_filter_date_start = ''

    send_filter_date_end = request.GET.get('filter_date_end')
    if send_filter_date_end is None:
        send_filter_date_end = ''

    context = {
        'select_menu': 'reports',
        'chart_line': chart_line,
        'chart_bar_plus': chart_bar_plus,
        'chart_bar_minus': chart_bar_minus,
        'filter_date_start': send_filter_date_start,
        'filter_date_end': send_filter_date_end,
    }
    return render(request, 'andr_finance/reports_chart.html', context)


def my_settings(request):
    if request.method == 'GET':
        load_demo = request.GET.get('load_demo')
        if load_demo == 'load_demo':
            load_demo_data()

    context = {
        'select_menu': 'my_settings',
    }
    return render(request, 'andr_finance/my_settings.html', context)

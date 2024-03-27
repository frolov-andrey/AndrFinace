import logging
import os

# from ..my_finance.settings import BASE_DIR
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CategoryForm, AccountForm, TransactionFormMinusPlus, TransactionFormTransfer
from .models import Account, Category, Transaction

# todo: это правильно?
logger = logging.getLogger(__name__)

folders = [
    {'name': 'finance', 'name_rus': 'Финансы'},
    {'name': 'foot', 'name_rus': 'Еда'},
]


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
    BASE_DIR = settings.BASE_DIR
    logger.debug('BASE_DIR = ' + str(BASE_DIR))
    context = {'select_menu': 'index'}
    return render(request, 'andr_finance/index.html', context)


# --- Category ---
def categories(request):
    categories = Category.objects.order_by('name')
    context = {
        'categories': categories,
        'select_menu': 'categories',
    }
    return render(request, 'andr_finance/categories.html', context)


def category_add(request):
    images_path = str(settings.STATIC_URL) + 'andr_finance/images/'
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
    images_path = str(settings.STATIC_URL) + 'andr_finance/images/'
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
def get_balance(account_id):
    balance = 0
    transactions = Transaction.objects.filter(account_id=account_id)
    for transaction in transactions:
        # todo: Int + Decimal ?
        balance = balance + transaction.amount

    return balance


def accounts(request):
    accounts = Account.objects.order_by('name')
    context_accounts = []
    for account in accounts:
        balance = get_balance(account.id)

        # todo: Так можно?:
        account.balance = balance

        o_account = {'account': account, 'balance': balance}
        context_accounts.append(o_account)

    context = {
        'context_accounts': context_accounts,
        'select_menu': 'accounts',
    }

    return render(request, 'andr_finance/accounts.html', context)


def account_add(request):
    if request.method != 'POST':
        form = AccountForm
    else:
        form = AccountForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:accounts')

    context = {
        'form': form,
        'select_menu': 'accounts',
    }
    return render(request, 'andr_finance/account_add.html', context)


def account_edit(request, account_id):
    account = Account.objects.get(id=account_id)

    if request.method != 'POST':
        form = AccountForm(instance=account)
    else:
        form = AccountForm(instance=account, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:accounts')

    context = {
        'account': account,
        'form': form,
        'select_menu': 'accounts',
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
    filter_account = request.GET.get('filter_account')

    if (request.method == 'GET'
            and filter_account is not None
            and filter_account != '0'):
        transactions = Transaction.objects.filter(account=filter_account, type_transaction=Transaction.MINUS).order_by(
            'date_added')
    else:
        transactions = Transaction.objects.order_by('date_added')

    total_amount = transactions.aggregate(Sum('amount'))['amount__sum']
    # print(total_amount)

    context = {
        'transactions': transactions,
        'accounts': Account.objects.order_by('name'),
        'select_menu': 'transactions',
        'filter_account': filter_account,
        'total_amount': total_amount,
    }

    return render(request, 'andr_finance/transactions.html', context)


def transaction_add(request, type_transaction):
    # logger.debug('type_transaction = ' + str(type_transaction))
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

    # todo: Возможно тут проблемка
    if request.method == 'POST' or request.method == 'GET':
        transaction.delete()
        messages.success(
            request,
            'The transaction has been deleted successfully: ' +
            transaction.date_added.strftime('%d.%m.%Y %H:%M')
        )
        return redirect('andr_finance:transactions')


def reports(request):
    context = {}
    return render(request, 'andr_finance/reports.html', context)

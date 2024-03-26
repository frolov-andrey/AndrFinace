import logging

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CategoryForm, AccountForm, TransactionFormMinusPlus, TransactionFormTransfer
from .models import Account, Category, Transaction

# todo: это правильно?
logger = logging.getLogger(__name__)


def page_not_found(request):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def index(request):
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
    if request.method != 'POST':
        form = CategoryForm
    else:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:categories')

    context = {
        'form': form,
        'select_menu': 'categories',
    }
    return render(request, 'andr_finance/category_add.html', context)


def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = CategoryForm(instance=category)
    else:
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:categories')

    context = {
        'category': category,
        'form': form,
        'select_menu': 'categories',
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
        transactions = Transaction.objects.filter(account=filter_account, change=Transaction.MINUS).order_by(
            'date_added')
    else:
        transactions = Transaction.objects.order_by('date_added')

    total_amount = transactions.aggregate(Sum('amount'))['amount__sum']
    print(total_amount)

    context = {
        'transactions': transactions,
        'accounts': Account.objects.order_by('name'),
        'select_menu': 'transactions',
        'filter_account': filter_account,
        'total_amount': total_amount,
    }

    return render(request, 'andr_finance/transactions.html', context)


def transaction_add(request, type_transaction):
    logger.debug('type_transaction = ' + str(type_transaction))
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
            elif type_transaction == Transaction.PLUS:
                transaction.type_transaction = Transaction.PLUS
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


# def transaction_add_minus(request):
#     if request.method != 'POST':
#         form = TransactionFormMinus()
#     else:
#         form = TransactionFormMinus(data=request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             form.change = Transaction.MINUS
#             form.save()
#             return redirect('andr_finance:transactions')
#
#     context = {
#         'form': form,
#         'select_menu': 'transactions',
#         'type_transaction': Transaction.MINUS,
#     }
#     return render(request, 'andr_finance/transaction_add.html', context)


def transaction_edit(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method != 'POST':
        form = TransactionForm(instance=transaction)
    else:
        form = TransactionForm(instance=transaction, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:transactions')

    context = {
        'transaction': transaction,
        'form': form,
        'select_menu': 'transactions',
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

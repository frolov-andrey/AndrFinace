from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Account, Category, Currency, Transaction
from .forms import CategoryForm, CurrencyForm, AccountForm, TransactionForm


def index(request):
    return render(request, 'andr_finance/index.html')


# --- Category ---
def categories(request):
    categories = Category.objects.order_by('name')
    context = {'categories': categories}
    return render(request, 'andr_finance/categories.html', context)


def category_new(request):
    """ Определяем новую категорию. """
    if request.method != 'POST':
        # Данные не обновлялись, создается пустая форма
        form = CategoryForm
    else:
        # Отправлены данные POST, обрабатывать данные
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:categories')

    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'andr_finance/category_new.html', context)


def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = CategoryForm(instance=category)
    else:
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:categories')

    context = {'category': category, 'form': form}
    return render(request, 'andr_finance/category_edit.html', context)


def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {'category': category}

    if request.method != 'POST':
        return render(request, 'andr_finance/category_edit.html', context)
    elif request.method == 'POST':
        category.delete()
        messages.success(request, 'The category has been deleted successfully: ' + category.name)
        return redirect('andr_finance:categories')


# --- Currency ---
def currencies(request):
    currencies = Currency.objects.order_by('name')
    context = {'currencies': currencies}
    return render(request, 'andr_finance/currencies.html', context)


def currency_new(request):
    if request.method != 'POST':
        form = CurrencyForm
    else:
        form = CurrencyForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:currencies')

    context = {'form': form}
    return render(request, 'andr_finance/currency_new.html', context)


def currency_edit(request, currency_id):
    currency = Currency.objects.get(id=currency_id)

    if request.method != 'POST':
        form = CurrencyForm(instance=currency)
    else:
        form = CurrencyForm(instance=currency, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:currencies')

    context = {'currency': currency, 'form': form}
    return render(request, 'andr_finance/currency_edit.html', context)


def currency_delete(request, currency_id):
    currency = get_object_or_404(Currency, pk=currency_id)
    context = {'currency': currency}

    if request.method != 'POST':
        return render(request, 'andr_finance/currency_edit.html', context)
    elif request.method == 'POST':
        currency.delete()
        messages.success(request, 'The currency has been deleted successfully: ' + currency.name)
        return redirect('andr_finance:currencies')


# --- Account ---
def accounts(request):
    accounts = Account.objects.order_by('name')
    context = {'accounts': accounts}
    return render(request, 'andr_finance/accounts.html', context)


def account_new(request):
    if request.method != 'POST':
        form = AccountForm
    else:
        form = AccountForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:accounts')

    context = {'form': form}
    return render(request, 'andr_finance/account_new.html', context)


def account_edit(request, account_id):
    account = Account.objects.get(id=account_id)

    if request.method != 'POST':
        form = AccountForm(instance=account)
    else:
        form = AccountForm(instance=account, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:accounts')

    context = {'account': account, 'form': form}
    return render(request, 'andr_finance/account_edit.html', context)


def account_delete(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    context = {'account': account}

    if request.method != 'POST':
        return render(request, 'andr_finance/account_edit.html', context)
    elif request.method == 'POST':
        account.delete()
        messages.success(request, 'The currency has been deleted successfully: ' + account.name)
        return redirect('andr_finance:accounts')


# --- Transaction ---
def transactions(request):
    transactions = Transaction.objects.order_by('date_added')
    context = {'transactions': transactions}
    return render(request, 'andr_finance/transactions.html', context)


def transaction_new(request):
    if request.method != 'POST':
        form = TransactionForm
    else:
        form = TransactionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:transactions')

    context = {'form': form}
    return render(request, 'andr_finance/transaction_new.html', context)


def transaction_edit(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method != 'POST':
        form = TransactionForm(instance=transaction)
    else:
        form = TransactionForm(instance=transaction, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:transactions')

    context = {'transaction': transaction, 'form': form}
    return render(request, 'andr_finance/transaction_edit.html', context)


def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    context = {'transaction': transaction}

    if request.method == 'GET':
        return render(request, 'andr_finance/transaction_delete.html', context)
    elif request.method == 'POST':
        transaction.delete()
        messages.success(
            request,
            'The transaction has been deleted successfully: ' +
            transaction.date_added.strftime('%d.%m.%Y %H:%M')
        )
        return redirect('andr_finance:transactions')

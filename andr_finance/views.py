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


def new_category(request):
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
    return render(request, 'andr_finance/new_category.html', context)


def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = CategoryForm(instance=category)
    else:
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:categories')

    context = {'category': category, 'form': form}
    return render(request, 'andr_finance/edit_category.html', context)


def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {'category': category}

    if request.method != 'POST':
        return render(request, 'andr_finance/edit_category.html', context)
    elif request.method == 'POST':
        category.delete()
        messages.success(request, 'The category has been deleted successfully: ' + category.name)
        return redirect('andr_finance:categories')


# --- Currency ---
def currencies(request):
    currencies = Currency.objects.order_by('name')
    context = {'currencies': currencies}
    return render(request, 'andr_finance/currencies.html', context)


def new_currency(request):
    if request.method != 'POST':
        form = CurrencyForm
    else:
        form = CurrencyForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:currencies')

    context = {'form': form}
    return render(request, 'andr_finance/new_currency.html', context)


def edit_currency(request, currency_id):
    currency = Currency.objects.get(id=currency_id)

    if request.method != 'POST':
        form = CurrencyForm(instance=currency)
    else:
        form = CurrencyForm(instance=currency, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:currencies')

    context = {'currency': currency, 'form': form}
    return render(request, 'andr_finance/edit_currency.html', context)


# --- Account ---
def accounts(request):
    accounts = Account.objects.order_by('name')
    context = {'accounts': accounts}
    return render(request, 'andr_finance/accounts.html', context)


def new_account(request):
    if request.method != 'POST':
        form = AccountForm
    else:
        form = AccountForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:accounts')

    context = {'form': form}
    return render(request, 'andr_finance/new_account.html', context)


def edit_account(request, account_id):
    account = Account.objects.get(id=account_id)

    if request.method != 'POST':
        form = AccountForm(instance=account)
    else:
        form = AccountForm(instance=account, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:accounts')

    context = {'account': account, 'form': form}
    return render(request, 'andr_finance/edit_account.html', context)


# --- Transaction ---
def transactions(request):
    transactions = Transaction.objects.order_by('date_added')
    context = {'transactions': transactions}
    return render(request, 'andr_finance/transactions.html', context)


def new_transaction(request):
    if request.method != 'POST':
        form = TransactionForm
    else:
        form = TransactionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:transactions')

    context = {'form': form}
    return render(request, 'andr_finance/new_transaction.html', context)


def edit_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method != 'POST':
        form = TransactionForm(instance=transaction)
    else:
        form = TransactionForm(instance=transaction, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('andr_finance:transactions')

    context = {'transaction': transaction, 'form': form}
    return render(request, 'andr_finance/edit_transaction.html', context)


def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    context = {'transaction': transaction}

    if request.method == 'GET':
        return render(request, 'andr_finance/delete_transaction.html', context)
    elif request.method == 'POST':
        transaction.delete()
        messages.success(
            request,
            'The transaction has been deleted successfully: ' +
            transaction.date_added.strftime('%d.%m.%Y %H:%M')
        )
        return redirect('andr_finance:transactions')

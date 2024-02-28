from django.shortcuts import render, redirect

from .models import Account, Category, Currency
from .forms import CategoryForm, CurrencyForm


def index(request):
    return render(request, 'andr_finance/index.html')


def accounts(request):
    accounts = Account.objects.order_by('name')
    context = {'accounts': accounts}
    return render(request, 'andr_finance/accounts.html', context)


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

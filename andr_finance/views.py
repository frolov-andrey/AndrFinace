from django.shortcuts import render, redirect

from .models import Account, Category
from .forms import CategoryForm


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

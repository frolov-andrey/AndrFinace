import json
import os
from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from .demo import load_demo_data
from .forms import TransactionFormMinusPlus, TransactionFormTransfer
from .models import Account, Category, Transaction
from .report_chart import get_chart_line, get_chart_bar, get_chart_str, get_min_max_date, get_labels, \
    get_chart_bar_category
from .report_table import get_filter_transaction, get_transaction, get_transactions_group, get_balances, \
    get_sum_transaction

type_transactions = [
    {'code': Transaction.MINUS, 'name': Transaction.TYPE_TRANSACTION[0][1]},
    {'code': Transaction.PLUS, 'name': Transaction.TYPE_TRANSACTION[1][1]},
    {'code': Transaction.TRANSFER, 'name': Transaction.TYPE_TRANSACTION[2][1]},
]

folders = [
    {'name': 'finance', 'name_rus': 'Финансы'},
    {'name': 'people', 'name_rus': 'Люди'},
    {'name': 'foot', 'name_rus': 'Еда'},
    {'name': 'animals', 'name_rus': 'Животные'},
    {'name': 'different', 'name_rus': 'Разное'},
]
images_path = str(settings.STATIC_URL) + 'andr_finance/item_images/'
icon_default = images_path + 'default/default_icon.png'


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Преобразуем Decimal в строку
        return super().default(obj)


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


class Home(TemplateView):
    template_name = "andr_finance/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'index'
        return context


@login_required
def reports(request):
    if request.GET.get('chart_select') is None:
        chart_select = 'cash_flow'
    else:
        chart_select = request.GET.get('chart_select')

    if request.GET.get('second') is None:
        # Получаем текущую дату
        current_date = datetime.now()

        # Получаем первый день текущего месяца
        first_day_of_month = current_date.replace(day=1)

        # Получаем первый день следующего месяца
        # Добавляем 4 дня, чтобы перейти на следующий месяц
        next_month = current_date.replace(day=28) + timedelta(days=4)
        first_day_of_next_month = next_month.replace(day=1)

        # Получаем последний день текущего месяца (последний день предыдущего месяца)
        last_day_of_month = first_day_of_next_month - timedelta(days=1)

        send_filter_date_start = first_day_of_month.strftime("%d.%m.%Y")
        send_filter_date_end = last_day_of_month.strftime("%d.%m.%Y")
    else:
        send_filter_date_start = request.GET.get('filter_date_start')
        if send_filter_date_start is None:
            send_filter_date_start = ''

        send_filter_date_end = request.GET.get('filter_date_end')
        if send_filter_date_end is None:
            send_filter_date_end = ''

    filters = get_filter_transaction(request)
    if request.GET.get('second') is None:
        if 'date_start' not in filters and 'date_end' not in filters:
            if send_filter_date_start != '' and send_filter_date_end != '':
                filters['date_start'] = datetime.strptime(send_filter_date_start, '%d.%m.%Y')
                filters['date_end'] = datetime.strptime(send_filter_date_end, '%d.%m.%Y') + timedelta(days=1)

    transactions = get_transaction(filters, request)

    charts = {}
    if chart_select == 'cash_flow':
        transactions_by_date_plus = get_chart_bar(filters, transactions, Transaction.PLUS)
        transactions_by_date_minus = get_chart_bar(filters, transactions, Transaction.MINUS)

        min_date, max_date = get_min_max_date(filters, transactions_by_date_plus, transactions_by_date_minus)

        chart_bar_plus = get_chart_str(filters, transactions_by_date_plus, Transaction.PLUS, min_date, max_date)
        chart_bar_minus = get_chart_str(filters, transactions_by_date_minus, Transaction.MINUS, min_date, max_date)

        chart_line = get_chart_line(filters, transactions_by_date_plus, transactions_by_date_minus, min_date, max_date)

        labels = get_labels(min_date, max_date)

        charts = {
            'bar_plus': chart_bar_plus,
            'bar_minus': chart_bar_minus,
            'line': chart_line,
            'labels': labels,
        }

    elif chart_select == 'by_category':
        chart_bar_category = get_chart_bar_category(transactions)
        charts = {
            'chart_bar_category': chart_bar_category
        }

    context = {
        'select_menu': 'reports',
        'charts': charts,
        'chart_select': chart_select,
        'accounts': Account.objects.order_by('name'),

        'filter_account': request.GET.get('filter_account'),
        'filter_date_start': send_filter_date_start,
        'filter_date_end': send_filter_date_end,
    }

    return render(request, 'andr_finance/reports_chart.html', context)


@login_required
def my_settings(request):
    if request.method == 'GET':
        load_demo = request.GET.get('load_demo')
        if load_demo == 'load_demo':
            load_demo_data(request.user.id)

    context = {
        'select_menu': 'my_settings',
    }
    return render(request, 'andr_finance/my_settings.html', context)

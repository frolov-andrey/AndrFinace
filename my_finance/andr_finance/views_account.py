from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import AccountForm
from .models import Account
from .report_table import get_transaction, get_sum_transaction
from .views import icon_default, get_images, images_path


class AccountView(ListView):
    template_name = 'andr_finance/accounts.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        balances = {}
        accounts = Account.objects.order_by('name')
        for account in accounts:
            if account.start_balance:
                balance = account.start_balance
            else:
                balance = Decimal(0)

            transactions = get_transaction({'account_id': account.id})
            sum_transaction = get_sum_transaction(transactions, {'account_id': account.id})
            balance = balance + sum_transaction
            balances[account.id] = balance

        context['balances'] = balances
        context['select_menu'] = 'accounts'
        context['icon_default'] = icon_default

        return context


class AccountAdd(CreateView):
    form_class = AccountForm
    template_name = 'andr_finance/account_add.html'
    success_url = reverse_lazy('andr_finance:accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        images = get_images(images_path)
        context['select_menu'] = 'accounts'
        context['images'] = images
        context['images_path'] = images_path
        context['image_default_folder'] = 'default'
        context['image_default_file'] = 'default_icon.png'

        return context

    def form_valid(self, form):
        account = form.save(commit=False)
        account.icon_folder = form.data['icon_folder']
        account.icon_file = form.data['icon_file']

        return super().form_valid(form)


class AccountUpdate(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'andr_finance/account_edit.html'
    success_url = reverse_lazy('andr_finance:accounts')

    title_page = 'Редактирование счета'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        images = get_images(images_path, self.object)

        context['select_menu'] = 'accounts',
        context['images'] = images
        context['images_path'] = images_path
        context['image_default_folder'] = 'default'
        context['image_default_file'] = 'default_icon.png'
        context['icon_file'] = self.object.icon_file
        context['icon_folder'] = self.object.icon_folder

        return context

    def form_valid(self, form):
        account = form.save(commit=False)
        account.icon_folder = form.data['icon_folder']
        account.icon_file = form.data['icon_file']

        return super().form_valid(form)


class AccountDelete(DeleteView):
    model = Account
    success_url = reverse_lazy("andr_finance:accounts")

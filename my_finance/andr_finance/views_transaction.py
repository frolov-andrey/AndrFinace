from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TransactionFormMinusPlus, TransactionFormTransfer
from .models import Account, Category, Transaction
from .report_table import get_filter_transaction, get_transactions_group, get_transaction, get_balances, \
    get_sum_transaction
from .views import type_transactions, icon_default, page_not_found, get_images, images_path


class TransactionView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'andr_finance/transactions.html'
    context_object_name = 'transactions'

    # def get_queryset(self):
    #     return Transaction.objects.filter(user=self.request.user).order_by('date_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filters = get_filter_transaction(self.request)

        if 'filter_group_category' in filters:
            group_by = filters['filter_group_category']
            transactions_group = get_transactions_group(filters, self)
        else:
            group_by = ''
            transactions_group = []

        transactions = get_transaction(filters, self.request)
        balances = get_balances(transactions, filters, self.request)

        send_filter_date_start = self.request.GET.get('filter_date_start')
        if send_filter_date_start is None:
            send_filter_date_start = ''

        send_filter_date_end = self.request.GET.get('filter_date_end')
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

        total_sum = get_sum_transaction(transactions, filters)

        context['sort_field'] = sort_field
        context['sort_order'] = sort_order
        context['group_by'] = group_by
        context['transactions'] = transactions
        context['balances'] = balances
        context['transactions_group'] = transactions_group
        context['accounts'] = Account.objects.order_by('name')
        context['categories'] = Category.objects.order_by('name')
        context['type_transactions'] = type_transactions
        context['select_menu'] = 'transactions'
        context['icon_default'] = icon_default
        context['total_sum'] = total_sum

        context['filter_account'] = self.request.GET.get('filter_account')
        context['filter_category'] = self.request.GET.get('filter_category')
        context['filter_type_transaction'] = self.request.GET.get('filter_type_transaction')
        context['filter_date_start'] = send_filter_date_start
        context['filter_date_end'] = send_filter_date_end
        context['filter_group_category'] = self.request.GET.get('filter_group_category')

        return context


class TransactionAddPlus(LoginRequiredMixin, CreateView):
    form_class = TransactionFormMinusPlus
    template_name = 'andr_finance/transaction_add.html'
    success_url = reverse_lazy('andr_finance:transactions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'transactions'
        context['type_transaction'] = Transaction.PLUS

        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.type_transaction = Transaction.PLUS
        transaction.account_recipient = None

        return super().form_valid(form)


class TransactionAddMinus(LoginRequiredMixin, CreateView):
    form_class = TransactionFormMinusPlus
    template_name = 'andr_finance/transaction_add.html'
    success_url = reverse_lazy('andr_finance:transactions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'transactions'
        context['type_transaction'] = Transaction.MINUS

        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.type_transaction = Transaction.MINUS
        transaction.account_recipient = None

        return super().form_valid(form)


class TransactionAddTransfer(LoginRequiredMixin, CreateView):
    form_class = TransactionFormTransfer
    template_name = 'andr_finance/transaction_add.html'
    success_url = reverse_lazy('andr_finance:transactions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'transactions'
        context['type_transaction'] = Transaction.TRANSFER

        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.type_transaction = Transaction.TRANSFER

        return super().form_valid(form)


class TransactionUpdatePlus(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionFormMinusPlus
    template_name = 'andr_finance/transaction_edit.html'
    success_url = reverse_lazy('andr_finance:transactions')

    title_page = 'Редактирование транзакции'

    def get_object(self, queryset=None):
        transaction = super().get_object(queryset)
        if transaction.user != self.request.user:
            raise Http404("Транзакция не существует или у вас нет разрешения на доступ к ней")
        return transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'transactions'
        context['type_transaction'] = Transaction.PLUS

        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.type_transaction = Transaction.PLUS
        transaction.account_recipient = None

        return super().form_valid(form)


class TransactionUpdateMinus(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionFormMinusPlus
    template_name = 'andr_finance/transaction_edit.html'
    success_url = reverse_lazy('andr_finance:transactions')

    title_page = 'Редактирование транзакции'

    def get_object(self, queryset=None):
        transaction = super().get_object(queryset)
        if transaction.user != self.request.user:
            raise Http404("Транзакция не существует или у вас нет разрешения на доступ к ней")
        return transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'transactions'
        context['type_transaction'] = Transaction.MINUS

        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.type_transaction = Transaction.MINUS
        transaction.account_recipient = None

        return super().form_valid(form)


class TransactionUpdateTransfer(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionFormTransfer
    template_name = 'andr_finance/transaction_edit.html'
    success_url = reverse_lazy('andr_finance:transactions')

    title_page = 'Редактирование транзакции'

    def get_object(self, queryset=None):
        transaction = super().get_object(queryset)
        if transaction.user != self.request.user:
            raise Http404("Транзакция не существует или у вас нет разрешения на доступ к ней")
        return transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'transactions'
        context['type_transaction'] = Transaction.TRANSFER

        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.type_transaction = Transaction.TRANSFER

        return super().form_valid(form)


class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy("andr_finance:transactions")

    def get_object(self, queryset=None):
        transaction = super().get_object(queryset)
        if transaction.user != self.request.user:
            raise Http404("Транзакция не существует или у вас нет разрешения на доступ к ней")
        return transaction

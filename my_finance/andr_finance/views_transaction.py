from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TransactionFormMinusPlus, TransactionFormTransfer
from .models import Account, Category, Transaction
from .report_table import get_filter_transaction, get_transactions_group, get_transaction, get_balances, \
    get_sum_transaction
from .views import type_transactions, icon_default, page_not_found, get_images, images_path


class TransactionView(ListView):
    template_name = 'andr_finance/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.order_by('date_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filters = get_filter_transaction(self.request)

        if 'filter_group_category' in filters:
            group_by = filters['filter_group_category']
            transactions_group = get_transactions_group(filters)
        else:
            group_by = ''
            transactions_group = []

        transactions = get_transaction(filters)
        balances = get_balances(transactions, filters)

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


class TransactionAddPlus(CreateView):
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


class TransactionAddMinus(CreateView):
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


class TransactionAddTransfer(CreateView):
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


class TransactionUpdatePlus(UpdateView):
    model = Transaction
    form_class = TransactionFormMinusPlus
    template_name = 'andr_finance/transaction_edit.html'
    success_url = reverse_lazy('andr_finance:transactions')

    title_page = 'Редактирование транзакции'

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


class TransactionUpdateMinus(UpdateView):
    model = Transaction
    form_class = TransactionFormMinusPlus
    template_name = 'andr_finance/transaction_edit.html'
    success_url = reverse_lazy('andr_finance:transactions')

    title_page = 'Редактирование транзакции'

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


class TransactionUpdateTransfer(UpdateView):
    model = Transaction
    form_class = TransactionFormTransfer
    template_name = 'andr_finance/transaction_edit.html'
    success_url = reverse_lazy('andr_finance:transactions')

    title_page = 'Редактирование транзакции'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'transactions'
        context['type_transaction'] = Transaction.TRANSFER

        return context

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.type_transaction = Transaction.TRANSFER

        return super().form_valid(form)


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


class TransactionDelete(DeleteView):
    model = Transaction
    success_url = reverse_lazy("andr_finance:transactions")

from django import forms
from django.forms import TextInput, NumberInput, Select

from .models import Category, Account, Transaction


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Название', widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = ['name']


class AccountForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        label='Название',
        widget=TextInput(attrs={'class': 'form-select'})
    )
    start_balance = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Начальный баланс',
        widget=NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Account
        fields = ['name', 'start_balance']


class TransactionFormTransfer(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all().order_by('name'),
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Счет отправитель'
    )
    account_recipient = forms.ModelChoiceField(
        queryset=Account.objects.all().order_by('name'),
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Счет получатель'
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Сумма',
        widget=NumberInput(attrs={'class': 'form-control mb-3'})
    )
    date_added = forms.DateTimeField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'readonly': 'readonly', 'class': 'form-control mb-3'}),
        label='Дата'
    )
    category = forms.ModelChoiceField(Category.objects.all().order_by('name'), widget=Select(attrs={'class': 'form-select mb-3'}),
                                      label='Категория')
    title = forms.CharField(max_length=200, label='Описание', widget=TextInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = Transaction
        fields = ['account', 'account_recipient', 'amount', 'date_added', 'category', 'title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['title'].required = False


class TransactionFormMinusPlus(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all().order_by('name'),
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Счет'
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Сумма',
        widget=NumberInput(attrs={'class': 'form-control mb-3'})
    )
    date_added = forms.DateTimeField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'readonly': 'readonly', 'class': 'form-control mb-3'}),
        label='Дата'
    )
    category = forms.ModelChoiceField(Category.objects.all().order_by('name'), widget=Select(attrs={'class': 'form-select mb-3'}),
                                      label='Категория')
    title = forms.CharField(max_length=200, label='Описание', widget=TextInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'date_added', 'category', 'title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['title'].required = False

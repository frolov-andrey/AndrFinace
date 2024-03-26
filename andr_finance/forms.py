from django import forms
from django.forms import TextInput, NumberInput, Select

from .models import Category, Currency, Account, Transaction


class CurrencyForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Название', widget=TextInput(attrs={'class': 'form-control'}))
    code = forms.CharField(max_length=200, label='Код', widget=TextInput(attrs={'class': 'form-control'}))
    icon = forms.ImageField(label='Иконка')

    class Meta:
        model = Currency
        fields = ['name', 'code', 'icon']

    def __init__(self, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        self.fields['icon'].required = False


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
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        empty_label='Валюта не выбрана',
        label='Валюта',
        widget=Select(attrs={'class': 'form-select'})
    )
    icon = forms.ImageField(label='Иконка')

    class Meta:
        model = Account
        fields = ['name', 'start_balance', 'currency', 'icon']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['icon'].required = False


class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Счет'
    )
    account_recipient = forms.ModelChoiceField(
        queryset=Account.objects.all(),
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
        label='Дата создания'
    )
    category = forms.ModelChoiceField(Category.objects.all(), widget=Select(attrs={'class': 'form-select mb-3'}))
    title = forms.CharField(max_length=200, label='Описание', widget=TextInput(attrs={'class': 'form-control mb-3'}))
    description = forms.Textarea(attrs={'col': 80, 'class': 'form-control mb-3'})
    change = forms.ChoiceField(
        choices=Transaction.CHANGE_CHOICES,
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Тип транзакции',
    )

    class Meta:
        model = Transaction
        fields = ['account', 'account_recipient', 'change', 'amount', 'date_added', 'category', 'title']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['account_recipient'].required = False
        self.fields['category'].required = False
        self.fields['title'].required = False

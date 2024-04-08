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
        queryset=Account.objects.none(),
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Счет отправитель'
    )
    account_recipient = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Счет получатель'
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Сумма',
        widget=NumberInput(attrs={'class': 'form-control mb-3'})
    )
    date_add = forms.DateTimeField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'readonly': 'readonly', 'class': 'form-control mb-3'}),
        label='Дата'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=Select(attrs={'class': 'form-select mb-3'}),
        label='Категория')
    title = forms.CharField(max_length=200, label='Описание', widget=TextInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = Transaction
        fields = ['account', 'account_recipient', 'amount', 'date_add', 'category', 'title']

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['title'].required = False
        self.fields['account'].queryset = Account.objects.filter(user=user_id).order_by('name')
        self.fields['account_recipient'].queryset = Account.objects.filter(user=user_id).order_by('name')
        self.fields['category'].queryset = Category.objects.filter(user=user_id).order_by('name')

class TransactionFormMinusPlus(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        widget=Select(attrs={'class': 'form-select mb-3 py-1'}),
        label='Счет'
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Сумма',
        widget=NumberInput(attrs={'class': 'form-control mb-3 py-1'})
    )
    date_add = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'autocomplete': 'off', 'format': '%d.%m.%Y %H:%i', 'class': 'form-control mb-3 py-1'}),
        label='Дата'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=Select(attrs={'class': 'form-select mb-3 py-1'}),
        label='Категория')
    title = forms.CharField(max_length=200, label='Описание',
                            widget=TextInput(attrs={'class': 'form-control mb-3 py-1'}))

    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'date_add', 'category', 'title']

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['title'].required = False
        self.fields['account'].queryset = Account.objects.filter(user=user_id).order_by('name')
        self.fields['category'].queryset = Category.objects.filter(user=user_id).order_by('name')


class MySettings(forms.Form):
    load_demo = forms.BooleanField()

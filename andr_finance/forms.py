from django import forms
from .models import Category, Currency, Account


class CurrencyForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    code = forms.CharField(max_length=200)
    icon = forms.ImageField()

    class Meta:
        model = Currency
        fields = ['name', 'code', 'icon']

    def __init__(self, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        self.fields['icon'].required = False


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=200)

    class Meta:
        model = Category
        fields = ['name']


class AccountForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    start_balance = forms.DecimalField(max_digits=12, decimal_places=2)
    icon = forms.ImageField()

    class Meta:
        model = Account
        fields = ['name', 'start_balance', 'currency', 'icon']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['icon'].required = False





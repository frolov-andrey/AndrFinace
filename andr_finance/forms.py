from django import forms
from .models import Category, Currency


class CurrencyForm(forms.ModelForm):
    name = forms.CharField(max_length=200)

    class Meta:
        model = Currency
        fields = ['name']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=200)

    class Meta:
        model = Category
        fields = ['name']






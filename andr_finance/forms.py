from django import forms
from .models import Category, Currency


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






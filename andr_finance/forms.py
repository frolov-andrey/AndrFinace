from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=200)

    class Meta:
        model = Category
        fields = ['name']



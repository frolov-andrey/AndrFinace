from django import forms
from .models import Category


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=200)




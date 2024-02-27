from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):

    # name = forms.CharField(max_length=200)
    # parent = forms.MultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['name', 'parent']

    # def __init__(self, *args, **kwargs):
    #     super(CategoryForm, self).__init__(*args, **kwargs)
    #     self.fields['parent'].required = False

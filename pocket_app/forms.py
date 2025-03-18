from django import forms
from .models import Category, Item


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_description', 'item_category',
                  'item_type', 'item_value', 'repeatability', 'repeatID']


CategoryFormSet = forms.modelformset_factory(
    Category, form=CategoryForm, extra=1)

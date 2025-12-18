# inventory/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'is_active']
        labels = {
            'name': 'اسم المنتج',
            'price': 'السعر',
            'is_active': 'متاح للبيع',
        }

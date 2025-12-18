from django import forms
from .models import TicketItem

class TicketItemForm(forms.ModelForm):
    class Meta:
        model = TicketItem
        fields = ['product', 'quantity']

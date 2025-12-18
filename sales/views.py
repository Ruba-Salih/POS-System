# sales/views.py
from django.shortcuts import render, redirect
from .forms import SaleForm

def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.cashier = request.user
            sale.save()
            return redirect('add_sale')
    else:
        form = SaleForm()

    return render(request, 'sales/add_sale.html', {'form': form})

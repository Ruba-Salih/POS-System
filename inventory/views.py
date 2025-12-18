# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product
from .forms import ProductForm
from pos_system.utils import is_manager


@login_required
def product_list(request):
    if is_manager(request.user):
        products = Product.objects.all()
    else:
        products = Product.objects.filter(is_active=True)

    return render(request, 'inventory/product_list.html', {
        'products': products
    })



@login_required
@user_passes_test(is_manager)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm()

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'title': 'إضافة منتج'
    })


@login_required
@user_passes_test(is_manager)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'title': 'تعديل منتج'
    })


@login_required
@user_passes_test(is_manager)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('inventory:product_list')


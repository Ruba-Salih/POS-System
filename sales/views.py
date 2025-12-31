from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

from .models import Ticket, TicketItem
from .forms import TicketItemForm
from inventory.models import Product

User = get_user_model()


# =========================
# CREATE NEW TICKET
# =========================
@login_required
def create_ticket(request):
    # ❌ لا ننشئ Ticket هنا
    # فقط نفتح صفحة POS
    return redirect('sales:pos')


# =========================
# POS VIEW (PER TICKET OR NEW)
# =========================
@login_required
def pos_view(request, ticket_id=None):
    ticket = None

    if ticket_id:
        ticket = get_object_or_404(
            Ticket,
            id=ticket_id,
            cashier=request.user,
            status='open'
        )

    products = Product.objects.filter(is_active=True)
    form = TicketItemForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        # ✅ إنشاء Ticket عند أول منتج فقط
        if ticket is None:
            ticket = Ticket.objects.create(
                cashier=request.user,
                status='open'
            )

        item = form.save(commit=False)
        item.ticket = ticket
        item.price = item.product.price
        item.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'ticket_id': ticket.id,
                'item': {
                    'id': item.id,
                    'product': item.product.name,
                    'price': float(item.price),
                    'quantity': item.quantity,
                    'subtotal': float(item.subtotal()),
                },
                'ticket_total': float(ticket.total_amount())
            })

        return redirect('sales:pos', ticket_id=ticket.id)

    return render(request, 'sales/pos.html', {
        'ticket': ticket,
        'products': products,
        'form': form
    })


# =========================
# CLOSE TICKET (AJAX)
# =========================
@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        cashier=request.user,
        status='open'
    )

    if not ticket.items.exists():
        return JsonResponse({'error': 'empty_ticket'}, status=400)

    payment_method = request.POST.get('payment_method')
    transfer_number = request.POST.get('transfer_number')

    if payment_method == 'transfer' and not transfer_number:
        return JsonResponse({'error': 'transfer_required'}, status=400)

    ticket.payment_method = payment_method
    ticket.transfer_number = transfer_number
    ticket.status = 'closed'
    ticket.save()

    return JsonResponse({
        'success': True,
        'ticket_id': ticket.id
    })


# =========================
# DELETE ITEM (MANAGER PIN)
# =========================
@login_required
def delete_ticket_item(request, item_id):
    item = get_object_or_404(
        TicketItem,
        id=item_id,
        ticket__cashier=request.user
    )
    ticket = item.ticket

    if ticket.status == 'closed':
        messages.error(request, 'لا يمكن تعديل طلب مغلق')
        return redirect('sales:pos', ticket_id=ticket.id)

    if request.method == 'POST':
        manager_pin = request.POST.get('manager_pin')

        manager = User.objects.filter(
            role='manager',
            manager_pin__isnull=False
        ).first()

        if not manager or not check_password(manager_pin, manager.manager_pin):
            messages.error(request, 'رمز المدير غير صحيح')
            return redirect('sales:pos', ticket_id=ticket.id)

        item.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'ticket_total': float(ticket.total_amount())
            })

        # 🧹 لو حذف آخر عنصر → احذف Ticket
        if not ticket.items.exists():
            ticket.delete()
            return redirect('cashier_dashboard')

    return redirect('sales:pos', ticket_id=ticket.id)


# =========================
# UPDATE QUANTITY (AJAX)
# =========================
@login_required
def update_ticket_item(request, item_id):
    item = get_object_or_404(
        TicketItem,
        id=item_id,
        ticket__cashier=request.user
    )
    ticket = item.ticket

    if ticket.status == 'closed':
        return JsonResponse({'error': 'ticket_closed'}, status=400)

    quantity = request.POST.get('quantity')

    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'invalid_quantity'}, status=400)

    item.quantity = quantity
    item.save()

    return JsonResponse({
        'item_subtotal': float(item.subtotal()),
        'ticket_total': float(ticket.total_amount())
    })


# =========================
# PRINT RECEIPT
# =========================
@login_required
def print_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    return render(request, 'sales/receipt.html', {
        'ticket': ticket
    })

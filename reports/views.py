from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from django.contrib import messages
from pos_system.utils import business_day_range

from sales.models import Ticket, TicketItem
from pos_system.utils import is_manager
from expenses.models import Expense

@user_passes_test(is_manager)
def dashboard(request):
    tickets = Ticket.objects.filter(
        status='closed',items__isnull=False).distinct()

    day = request.GET.get('day')
    month = request.GET.get('month')

    if day:
        day = datetime.strptime(day, "%Y-%m-%d").date()
        start, end = business_day_range(day)
        tickets = tickets.filter(created_at__gte=start, created_at__lt=end)

    elif month:
        month = datetime.strptime(month, "%Y-%m").date()
        tickets = tickets.filter(
            created_at__year=month.year,
            created_at__month=month.month
        )

    else:
        start, end = business_day_range(now().date())
        tickets = tickets.filter(created_at__gte=start, created_at__lt=end)

    total_sales = sum(ticket.total_amount() for ticket in tickets)

    # ✅ إجمالي المصروفات لنفس الفترة
    expenses = Expense.objects.all()

    if day:
        expenses = expenses.filter(created_at__gte=start, created_at__lt=end)
    elif month:
        expenses = expenses.filter(
            created_at__year=month.year,
            created_at__month=month.month
        )
    else:
        expenses = expenses.filter(created_at__gte=start, created_at__lt=end)

    total_expenses = sum(e.amount for e in expenses)
    # ✅ الربح الصافي
    net_profit = total_sales - total_expenses

    context = {
        'tickets_count': tickets.count(),
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }

    return render(request, 'reports/dashboard.html', context)


@user_passes_test(is_manager)
def sales_list(request):
    tickets = Ticket.objects.select_related('cashier').filter(
        status='closed',
        items__isnull=False
        ).distinct()

    ref = request.GET.get('ref')
    day = request.GET.get('day')
    month = request.GET.get('month')

    if ref:
        tickets = tickets.filter(ref__iexact=ref)

    elif day:
        day = datetime.strptime(day, "%Y-%m-%d").date()
        start, end = business_day_range(day)
        tickets = tickets.filter(created_at__gte=start, created_at__lt=end)

    elif month:
        month = datetime.strptime(month, "%Y-%m").date()
        tickets = tickets.filter(
            created_at__year=month.year,
            created_at__month=month.month
        )

    elif not ref:
        start, end = business_day_range(now().date())
        tickets = tickets.filter(created_at__gte=start, created_at__lt=end)

    return render(request, 'reports/sales_list.html', {
        'tickets': tickets
    })


@user_passes_test(is_manager)
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    items = TicketItem.objects.filter(ticket=ticket).select_related('product')

    return render(request, 'reports/ticket_detail.html', {
        'ticket': ticket,
        'items': items
    })


@user_passes_test(is_manager)
def refund_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, status='closed')

    if request.method == 'POST':
        reason = request.POST.get('reason')

        ticket.status = 'refunded'
        ticket.refunded_at = now()
        ticket.refunded_by = request.user
        ticket.refund_reason = reason
        ticket.save()

        messages.success(request, 'تم إلغاء / إرجاع الطلب بنجاح')

    return redirect('reports:sales_list')

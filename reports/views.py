# reports/views.py
from django.shortcuts import render
from django.utils.timezone import now

def daily_report(request):
    today = now().date()

    sales_total = Sale.objects.filter(
        created_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    expenses_total = Expense.objects.filter(
        created_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    net = sales_total - expenses_total

    return render(request, 'reports/daily.html', {
        'sales_total': sales_total,
        'expenses_total': expenses_total,
        'net': net,
    })

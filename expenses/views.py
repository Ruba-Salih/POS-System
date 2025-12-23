from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from django.contrib import messages

from .models import Expense
from pos_system.utils import is_manager


@user_passes_test(is_manager)
def expense_list(request):
    expenses = Expense.objects.all().order_by('-created_at')

    day = request.GET.get('day')
    month = request.GET.get('month')

    if day:
        day = datetime.strptime(day, "%Y-%m-%d").date()
        expenses = expenses.filter(created_at__date=day)

    elif month:
        month = datetime.strptime(month, "%Y-%m").date()
        expenses = expenses.filter(
            created_at__year=month.year,
            created_at__month=month.month
        )

    else:
        expenses = expenses.filter(created_at__date=now().date())

    total_expenses = sum(e.amount for e in expenses)

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'total_expenses': total_expenses
    })

@user_passes_test(is_manager)
def add_expense(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if not description or not amount:
            messages.error(request, 'جميع الحقول مطلوبة')
            return redirect('expenses:add')

        Expense.objects.create(
            description=description,
            amount=amount,
            created_by=request.user
        )

        messages.success(request, 'تمت إضافة المصروف بنجاح')
        return redirect('expenses:list')

    return render(request, 'expenses/add_expense.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import (
    CustomUserCreationForm,
    CustomUserUpdateForm,
    CustomPasswordChangeForm,
    ManagerPinForm
)
from pos_system.utils import is_manager
from sales.models import Ticket


User = get_user_model()

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.role == 'manager':
                return redirect('manager_dashboard')
            elif user.role == 'cashier':
                return redirect('cashier_dashboard')
            else:
                return redirect('staff_dashboard')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')

    return render(request, 'staff/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/staff/login/')

@login_required
def manager_dashboard(request):
    return render(request, 'staff/manager_dashboard.html')

@login_required
def cashier_dashboard(request):
    open_tickets = Ticket.objects.filter(
        cashier=request.user,
        status='open',
        items__isnull=False
    ).distinct().order_by('-created_at')

    return render(request, 'staff/cashier_dashboard.html', {
        'open_ticket': open_tickets
    })

@login_required
def staff_home(request):
    return render(request, 'staff/cashier_dashboard.html')

@login_required
def staff_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'staff/user_list.html', {'users': users})

# إضافة مستخدم
@login_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة المستخدم بنجاح')
            return redirect('staff_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'staff/user_form.html', {
        'form': form,
        'title': 'إضافة مستخدم'
    })

# تعديل مستخدم
@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المستخدم')
            return redirect('staff_list')
    else:
        form = CustomUserUpdateForm(instance=user)

    return render(request, 'staff/user_form.html', {
        'form': form,
        'title': 'تعديل مستخدم'
    })

# حذف مستخدم
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'تم حذف المستخدم')
        return redirect('staff_list')

    return render(request, 'staff/user_delete.html', {'user': user})

# تغيير كلمة المرور
@login_required
def change_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'تم تغيير كلمة المرور بنجاح')

        # redirect back to correct dashboard
        if user.role == 'manager':
            return redirect('manager_dashboard')
        elif user.role == 'cashier':
            return redirect('cashier_dashboard')
        else:
            return redirect('staff_dashboard')

    return render(request, 'staff/change_password.html', {'form': form})

@login_required
def set_manager_pin(request):
    if not is_manager(request.user):
        return redirect('cashier_dashboard')

    form = ManagerPinForm(request.POST or None, instance=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, 'تم حفظ رمز المدير')
        return redirect('manager_dashboard')

    return render(request, 'staff/set_manager_pin.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'manager':
                return redirect('manager_dashboard')  # You’ll create this later
            elif user.role == 'cashier':
                return redirect('cashier_dashboard')  # You’ll create this later
            else:
                return redirect('home')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    return render(request, 'staff/login.html')

User = get_user_model()

@login_required
def staff_list(request):
    users = User.objects.all()
    return render(request, 'staff/user_list.html', {'users': users})

@login_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'staff/user_form.html', {'form': form})

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('users/', views.staff_list, name='staff_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/edit/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/cashier/', views.cashier_dashboard, name='pos_home'),
    path('dashboard/staff/', views.staff_home, name='staff_home'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.user_logout, name='logout'),

]

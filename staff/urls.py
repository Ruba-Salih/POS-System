from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('users/', views.staff_list, name='staff_list'),
    path('users/create/', views.create_user, name='create_user'),
]

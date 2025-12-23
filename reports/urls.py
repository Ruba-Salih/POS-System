from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('sales/<int:ticket_id>/refund/', views.refund_ticket, name='refund_ticket'),
]

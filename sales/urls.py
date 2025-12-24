from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # 🆕 POS بدون Ticket (طلب جديد فارغ)
    path('pos/', views.pos_view, name='pos'),

    # POS مع Ticket ID
    path('pos/<int:ticket_id>/', views.pos_view, name='pos'),

    # زر "طلب جديد"
    path('pos/new/', views.create_ticket, name='create_ticket'),

    # Ticket actions
    path('ticket/<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),
    path('item/delete/<int:item_id>/', views.delete_ticket_item, name='delete_ticket_item'),
    path('item/update/<int:item_id>/', views.update_ticket_item, name='update_ticket_item'),
    path('ticket/<int:ticket_id>/print/', views.print_ticket, name='print_ticket'),
]

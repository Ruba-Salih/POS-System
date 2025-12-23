from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('pos/<int:ticket_id>/', views.pos_view, name='pos'),
    path('pos/new/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),
    path('item/delete/<int:item_id>/', views.delete_ticket_item, name='delete_ticket_item'),
    path('item/update/<int:item_id>/', views.update_ticket_item, name='update_ticket_item'),
    path('ticket/<int:ticket_id>/print/', views.print_ticket, name='print_ticket'),
]

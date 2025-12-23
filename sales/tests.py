from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from sales.models import Ticket, TicketItem
from inventory.models import Product

User = get_user_model()


class POSTestCase(TestCase):

    def setUp(self):
        # Users
        self.cashier = User.objects.create_user(
            username='cashier',
            password='1234',
            role='cashier'
        )

        self.manager = User.objects.create_user(
            username='manager',
            password='1234',
            role='manager'
        )

        # Product
        self.product = Product.objects.create(
            name='Coffee',
            price=10,
            is_active=True
        )

        self.client.login(username='cashier', password='1234')

    def test_create_ticket(self):
        response = self.client.get(reverse('sales:create_ticket'))

        ticket = Ticket.objects.first()

        self.assertEqual(ticket.cashier, self.cashier)
        self.assertEqual(ticket.status, 'open')
        self.assertRedirects(
            response,
            reverse('sales:pos', args=[ticket.id])
        )

    def test_cashier_can_access_own_ticket(self):
        ticket = Ticket.objects.create(
            cashier=self.cashier,
            status='open'
        )

        response = self.client.get(
            reverse('sales:pos', args=[ticket.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_cashier_cannot_access_other_ticket(self):
        other = User.objects.create_user(
            username='other',
            password='1234',
            role='cashier'
        )

        ticket = Ticket.objects.create(
            cashier=other,
            status='open'
        )

        response = self.client.get(
            reverse('sales:pos', args=[ticket.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_add_item_to_ticket(self):
        ticket = Ticket.objects.create(
            cashier=self.cashier,
            status='open'
        )

        response = self.client.post(
            reverse('sales:pos', args=[ticket.id]),
            {
                'product': self.product.id,
                'quantity': 2
            }
        )

        self.assertEqual(ticket.items.count(), 1)

    def test_close_ticket_cash(self):
        ticket = Ticket.objects.create(
            cashier=self.cashier,
            status='open'
        )

        TicketItem.objects.create(
            ticket=ticket,
            product=self.product,
            quantity=1,
            price=10
        )

        response = self.client.post(
            reverse('sales:close_ticket', args=[ticket.id]),
            {
                'payment_method': 'cash'
            }
        )

        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'closed')

    def test_close_ticket_transfer_without_number_fails(self):
        ticket = Ticket.objects.create(
            cashier=self.cashier,
            status='open'
        )

        TicketItem.objects.create(
            ticket=ticket,
            product=self.product,
            quantity=1,
            price=10
        )

        response = self.client.post(
            reverse('sales:close_ticket', args=[ticket.id]),
            {
                'payment_method': 'transfer'
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_update_quantity(self):
        ticket = Ticket.objects.create(
            cashier=self.cashier,
            status='open'
        )

        item = TicketItem.objects.create(
            ticket=ticket,
            product=self.product,
            quantity=1,
            price=10
        )

        response = self.client.post(
            reverse('sales:update_ticket_item', args=[item.id]),
            {'quantity': 3}
        )

        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

    def test_cannot_update_closed_ticket(self):
        ticket = Ticket.objects.create(
            cashier=self.cashier,
            status='closed'
        )

        item = TicketItem.objects.create(
            ticket=ticket,
            product=self.product,
            quantity=1,
            price=10
        )

        response = self.client.post(
            reverse('sales:update_ticket_item', args=[item.id]),
            {'quantity': 3}
        )

        self.assertEqual(response.status_code, 400)

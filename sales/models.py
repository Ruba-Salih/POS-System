from django.db import models
from django.conf import settings
from inventory.models import Product
import uuid


class Ticket(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'نقداً'),
        ('transfer', 'تحويل'),
    )

    STATUS_CHOICES = (
        ('open', 'مفتوح'),
        ('closed', 'مغلق'),
    )

    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="الكاشير"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='open'
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        null=True,
        blank=True
    )
    transfer_number = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    ref = models.CharField(max_length=30, unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = f"{uuid.uuid4().hex[:6].upper()}"

        super().save(*args, **kwargs)

    def total_amount(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"طلب ({self.ref})"


class TicketItem(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # freeze price at time of sale
        if not self.pk:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def subtotal(self):
        return self.price * self.quantity

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('manager', 'مدير'),
        ('cashier', 'كاشير'),
        ('staff', 'موظف'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='staff')
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    manager_pin = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="رمز المدير"
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

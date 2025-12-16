from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('manager', 'مدير'),
        ('cashier', 'كاشير'),
        ('staff', 'موظف'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='staff')

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

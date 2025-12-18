# expenses/models.py
from django.db import models
from django.conf import settings

class Expense(models.Model):
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

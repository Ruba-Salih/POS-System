# inventory/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField("اسم المنتج", max_length=100)
    price = models.DecimalField("السعر", max_digits=10, decimal_places=2)
    is_active = models.BooleanField("متاح للبيع", default=True)

    def __str__(self):
        return self.name

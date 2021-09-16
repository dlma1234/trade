from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal("0.0")
    )


class Order(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.PROTECT, default=1)
    stock_id = models.ForeignKey(to=Stock, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal("0.0")
    )
    action = models.CharField(
        null=False, 
        choices=[
            ("buy", "Buy"),
            ("sell", "Sell")
        ],
        max_length=50
    )
    

from decimal import Decimal

from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal("0.0")
    )


class Order(models.Model):
    name = models.CharField(unique=True, max_length=255)
    stock_id = models.ForeignKey(to=Stock, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    action = models.CharField(
        null=False, 
        choices=[
            ("buy", "Buy"),
            ("sell", "Sell")
        ],
        default="new",
        max_length=50
    )

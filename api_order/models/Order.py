from django.db import models

from api_base.models import TimeStampedModel
from api_order.models import OrderStatus
from api_account.models import Account


class Order(TimeStampedModel):
    total_price = models.IntegerField()
    total_discount = models.IntegerField()
    shipping_address = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=20)
    done_at = models.DateTimeField(null=True, blank=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="order")

    class Meta:
        db_table = "order"
        ordering = ('-created_at',)

from django.db import models

from api_base.models import TimeStampedModel
from api_beer.models import Beer
from api_order.models import Order


class OrderDetail(TimeStampedModel):
    amount = models.PositiveIntegerField()
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name='order_detail')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail')

    class Meta:
        db_table = "order_detail"
        ordering = ('-created_at',)
        unique_together = ('beer', 'order')

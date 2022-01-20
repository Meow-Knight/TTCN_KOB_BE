from django.db import models

from api_base.models import TimeStampedModel
from api_order.models import OrderStatus, Order


class Progress(TimeStampedModel):
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, related_name='progress', null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='progress')

    class Meta:
        db_table = "progress"
        ordering = ('created_at',)

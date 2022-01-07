from django.db import models


class OrderStatus(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "order_status"
        ordering = ('id',)

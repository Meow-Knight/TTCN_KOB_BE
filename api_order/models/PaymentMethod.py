from django.db import models

from api_base.models import TimeStampedModel


class PaymentMethod(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "payment_method"
        ordering = ('id',)

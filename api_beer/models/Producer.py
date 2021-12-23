from django.db import models

from api_base.models import TimeStampedModel


class Producer(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)

    class Meta:
        db_table = "producer"
        ordering = ('name',)

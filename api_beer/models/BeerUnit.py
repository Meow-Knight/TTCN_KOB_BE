from django.db import models

from api_base.models import TimeStampedModel


class BeerUnit(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "beer_unit"
        ordering = ('name',)

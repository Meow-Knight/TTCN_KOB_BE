from django.db import models

from api_base.models import TimeStampedModel
from api_beer.models import Producer, Nation, BeerUnit


class Beer(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    alcohol_concentration = models.FloatField()
    capacity = models.CharField(max_length=50)
    origin_nation = models.ForeignKey(Nation, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.FloatField()
    bottle_amount = models.IntegerField(default=1)
    describe = models.TextField(null=True, blank=True)
    producer = models.ForeignKey(Producer, null=True, blank=True, on_delete=models.SET_NULL)
    beer_unit = models.ForeignKey(BeerUnit, on_delete=models.CASCADE)

    class Meta:
        db_table = "beer"
        ordering = ('name',)

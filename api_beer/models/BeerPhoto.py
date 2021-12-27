from django.db import models

from api_base.models import TimeStampedModel
from api_beer.models import Beer


class BeerPhoto(TimeStampedModel):
    link = models.CharField(max_length=200)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)

    class Meta:
        db_table = "beer_photo"

from django.db import models

from api_base.models import TimeStampedModel
from api_beer.models import Beer


class BeerShipment(TimeStampedModel):
    shipment_date = models.DateField()
    amount = models.IntegerField()
    price = models.FloatField()
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name="beer_shipment")

    class Meta:
        db_table = "beer_shipment"

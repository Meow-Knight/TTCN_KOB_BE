from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save

from api_base.models import TimeStampedModel
from api_beer.models import Beer


class BeerDiscount(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_activate = models.BooleanField(default=True)
    discount_percent = models.IntegerField()
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start should be before end')
        return super().clean()

    class Meta:
        db_table = "beer_discount"
        ordering = ('name',)

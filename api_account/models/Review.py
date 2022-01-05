from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from api_account.models import Account
from api_base.models import TimeStampedModel
from api_beer.models import Beer


class Review(TimeStampedModel):
    rate = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    comment = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)

    class Meta:
        db_table = "review"
        ordering = ('-updated_at',)
        unique_together = ('account', 'beer',)

from django.db import models

from api_base.models import TimeStampedModel
from api_beer.models import Beer
from api_account.models import Account


class Cart(TimeStampedModel):
    amount = models.IntegerField()
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name="cart")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cart")

    class Meta:
        db_table = "cart"
        ordering = ('-created_at',)
        unique_together = ('beer', 'account',)

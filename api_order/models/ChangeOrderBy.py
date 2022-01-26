from django.db import models

from api_account.models import Account
from api_base.models import TimeStampedModel
from api_order.models import Progress


class ChangeOrderBy(TimeStampedModel):
    progress = models.ForeignKey(Progress, on_delete=models.SET_NULL, related_name='change_order_by', null=True)
    staff = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='change_order_by', null=True)

    class Meta:
        db_table = "change_order_by"
        ordering = ('created_at', )

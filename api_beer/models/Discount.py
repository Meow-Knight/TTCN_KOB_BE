from django.core.exceptions import ValidationError
from django.db import models

from api_base.models import TimeStampedModel


class Discount(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_activate = models.BooleanField(default=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start should be before end')
        return super().clean()

    class Meta:
        db_table = "discount"
        ordering = ('name',)

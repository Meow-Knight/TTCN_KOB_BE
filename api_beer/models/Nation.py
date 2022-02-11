from django.db import models

from api_base.models import TimeStampedModel


class Nation(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    flag_picture = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "nation"
        ordering = ('name',)

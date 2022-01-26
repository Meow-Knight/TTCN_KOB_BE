import api_beer.constants.Data
import random
from datetime import datetime, timedelta

from django.db import migrations

import api_order.constants


def initial_data(apps, schema_editor):
    progress_model = apps.get_model("api_order", "Progress")
    staff_model = apps.get_model("api_account", "Account")
    change_order_by_model = apps.get_model("api_order", "ChangeOrderBy")

    cancel_status = api_order.constants.OrderStatus.CANCELED

    staffs = staff_model.objects.filter(is_staff=1)
    progresses = progress_model.objects.all().exclude(order_status__name=cancel_status.value.get("name"))

    change_order_by = []

    if progresses.exists() and staffs.exists():
        for progress in progresses:
            index_staff = random.randint(0, len(staffs) - 1)
            change_order_by.extend([change_order_by_model(created_at=progress.created_at,
                                                         updated_at=progress.updated_at,
                                                         progress=progress,
                                                         staff=staffs[index_staff])])

    change_order_by_model.objects.bulk_create(change_order_by)


class Migration(migrations.Migration):
    dependencies = [
        ('api_order', '0005_auto_20220124_2210'),
    ]

    operations = [
        migrations.RunPython(initial_data)
    ]

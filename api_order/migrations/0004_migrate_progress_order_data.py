from datetime import datetime, timedelta

from django.db import migrations
from django.utils import timezone

from api_order.constants import OrderStatus


def initial_data(apps, schema_editor):
    progress_model = apps.get_model("api_order", "Progress")
    order_status_model = apps.get_model("api_order", "OrderStatus")
    order_model = apps.get_model("api_order", "Order")

    completed_status = order_status_model.objects.get(name=OrderStatus.COMPLETED.value.get("name"))
    pending_status = order_status_model.objects.get(name=OrderStatus.PENDING.value.get("name"))
    delivering_status = order_status_model.objects.get(name=OrderStatus.DELIVERING.value.get("name"))
    delivered_status = order_status_model.objects.get(name=OrderStatus.DELIVERED.value.get("name"))
    confirmed_status = order_status_model.objects.get(name=OrderStatus.CONFIRMED.value.get("name"))
    canceled_status = order_status_model.objects.get(name=OrderStatus.CANCELED.value.get("name"))
    notreceivered_status = order_status_model.objects.get(name=OrderStatus.NOTRECEIVED.value.get("name"))

    orders = order_model.objects.all()
    progress_order = []

    if orders.exists():
        for order in orders:
            order_created_at = order.created_at
            order_updated_at = order.updated_at
            order_status = order.order_status.name
            if order_status == pending_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                     updated_at=order_updated_at,
                                                     order_status=pending_status,
                                                     order=order)])
            elif order_status == confirmed_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order)
                                       ])
            elif order_status == delivering_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order)
                                       ])
            elif order_status == delivered_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=3),
                                                      updated_at=order_updated_at + timedelta(days=3),
                                                      order_status=delivered_status,
                                                      order=order)
                                       ])
            elif order_status == completed_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=3),
                                                      updated_at=order_updated_at + timedelta(days=3),
                                                      order_status=delivered_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=4),
                                                      updated_at=order_updated_at + timedelta(days=4),
                                                      order_status=completed_status,
                                                      order=order)
                                       ])
            elif order_status == canceled_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=canceled_status,
                                                      order=order)
                                       ])
            elif order_status == notreceivered_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=3),
                                                      updated_at=order_updated_at + timedelta(days=3),
                                                      order_status=delivered_status,
                                                      order=order),
                                       progress_model(created_at=order_created_at + timedelta(days=4),
                                                      updated_at=order_updated_at + timedelta(days=4),
                                                      order_status=notreceivered_status,
                                                      order=order)
                                       ])

    progress_model.objects.bulk_create(progress_order)


def delete_all_data(apps, schema_editor):
    order_status_model = apps.get_model("api_order", "OrderStatus")
    order_model = apps.get_model("api_order", "Order")
    order_detail_model = apps.get_model("api_order", "OrderDetail")

    order_detail_model.objects.all().delete()
    order_model.objects.all().delete()
    order_status_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api_order', '0003_progress'),
    ]

    operations = [
        migrations.RunPython(initial_data, delete_all_data)
    ]

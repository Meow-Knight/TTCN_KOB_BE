import random
from datetime import datetime, timedelta

from django.db import migrations
from django.db.models import Q
from django.utils import timezone

from api_account.constants import RoleData
from api_order.constants import OrderStatus


def initial_data(apps, schema_editor):
    progress_model = apps.get_model("api_order", "Progress")
    order_status_model = apps.get_model("api_order", "OrderStatus")
    order_model = apps.get_model("api_order", "Order")
    account_model = apps.get_model("api_account", "Account")

    completed_status = order_status_model.objects.get(id=OrderStatus.COMPLETED.value.get("id"))
    pending_status = order_status_model.objects.get(id=OrderStatus.PENDING.value.get("id"))
    delivering_status = order_status_model.objects.get(id=OrderStatus.DELIVERING.value.get("id"))
    delivered_status = order_status_model.objects.get(id=OrderStatus.DELIVERED.value.get("id"))
    confirmed_status = order_status_model.objects.get(id=OrderStatus.CONFIRMED.value.get("id"))
    canceled_status = order_status_model.objects.get(id=OrderStatus.CANCELED.value.get("id"))
    notreceivered_status = order_status_model.objects.get(id=OrderStatus.NOTRECEIVED.value.get("id"))

    accounts = account_model.objects.filter(Q(role_id=RoleData.STAFF.value.get('id')) | Q(role_id=RoleData.ADMIN.value.get('id')))

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
                                                      order=order,
                                                      account=order.account)])
            elif order_status == confirmed_status.name:
                acc = accounts[random.randint(0, len(accounts) - 1)]
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order,
                                                      account=order.account),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order,
                                                      account=acc)
                                       ])
            elif order_status == delivering_status.name:
                acc = accounts[random.randint(0, len(accounts) - 1)]
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order,
                                                      account=order.account),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order,
                                                      account=acc)
                                       ])
            elif order_status == delivered_status.name:
                acc = accounts[random.randint(0, len(accounts) - 1)]
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order,
                                                      account=order.account),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=3),
                                                      updated_at=order_updated_at + timedelta(days=3),
                                                      order_status=delivered_status,
                                                      order=order,
                                                      account=acc)
                                       ])
            elif order_status == completed_status.name:
                acc = accounts[random.randint(0, len(accounts) - 1)]
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order,
                                                      account=order.account),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=3),
                                                      updated_at=order_updated_at + timedelta(days=3),
                                                      order_status=delivered_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=4),
                                                      updated_at=order_updated_at + timedelta(days=4),
                                                      order_status=completed_status,
                                                      order=order,
                                                      account=acc)
                                       ])
            elif order_status == canceled_status.name:
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order,
                                                      account=order.account),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=canceled_status,
                                                      order=order,
                                                      account=order.account)
                                       ])
            elif order_status == notreceivered_status.name:
                acc = accounts[random.randint(0, len(accounts))]
                progress_order.extend([progress_model(created_at=order_created_at,
                                                      updated_at=order_updated_at,
                                                      order_status=pending_status,
                                                      order=order,
                                                      account=order.account),
                                       progress_model(created_at=order_created_at + timedelta(days=1),
                                                      updated_at=order_updated_at + timedelta(days=1),
                                                      order_status=confirmed_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=2),
                                                      updated_at=order_updated_at + timedelta(days=2),
                                                      order_status=delivering_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=3),
                                                      updated_at=order_updated_at + timedelta(days=3),
                                                      order_status=delivered_status,
                                                      order=order,
                                                      account=acc),
                                       progress_model(created_at=order_created_at + timedelta(days=4),
                                                      updated_at=order_updated_at + timedelta(days=4),
                                                      order_status=notreceivered_status,
                                                      order=order,
                                                      account=order.account)
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

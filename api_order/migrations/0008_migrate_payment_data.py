import random

from django.db import migrations

from api_order.constants.Data import PaymentMethod


def initial_data(apps, schema_editor):
    payment_model = apps.get_model("api_order", "Payment")
    payment_method_model = apps.get_model("api_order", "PaymentMethod")
    order_model = apps.get_model("api_order", "Order")

    direct = payment_method_model.objects.get(name=PaymentMethod.DIRECT.value.get("name"))
    paypal = payment_method_model.objects.get(name=PaymentMethod.PAYPAL.value.get("name"))
    orders = order_model.objects.all()

    payments = []

    if orders.exists():
        for order in orders:
            if random.choice([True, False]):
                payments.extend([payment_model(created_at=order.created_at,
                                               updated_at=order.updated_at,
                                               order=order,
                                               payment_method=direct)])
            else:
                payments.extend([payment_model(created_at=order.created_at,
                                               updated_at=order.updated_at,
                                               order=order,
                                               payment_method=paypal,
                                               id_paypal="ARDFW6WJWMSS4",
                                               email_paypal=order.account.email)])

    payment_model.objects.bulk_create(payments)


def delete_all_data(apps, schema_editor):
    payment_model = apps.get_model("api_order", "Payment")

    payment_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("api_order", "0007_payment"),
    ]

    operations = [
        migrations.RunPython(initial_data, delete_all_data)
    ]
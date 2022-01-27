from django.db import migrations

from api_order.constants.Data import PaymentMethod


def initial_data(apps, schema_editor):
    payment_method_model = apps.get_model("api_order", "PaymentMethod")

    payment_method = map(lambda pay_method: payment_method_model(id=pay_method.value.get("id"), name=pay_method.value.get("name")),
                         PaymentMethod)

    payment_method_model.objects.bulk_create(payment_method)


def delete_all_data(apps, schema_editor):
    payment_method_model = apps.get_model("api_order", "PaymentMethod")

    payment_method_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api_order', '0005_paymentmethod'),
    ]

    operations = [
        migrations.RunPython(initial_data, delete_all_data)
    ]
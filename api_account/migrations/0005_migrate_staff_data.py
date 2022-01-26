import os
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.db import migrations


def initial_data(apps, schema_editor):
    account_model = apps.get_model("api_account", "Account")
    role_model = apps.get_model("api_account", "Role")

    staff_role = role_model.objects.filter(name="STAFF").first()

    staffs = []

    staffs.extend([account_model(is_superuser=False, first_name="Nguyen", last_name="Van Tan", is_staff=True,
                            username="nguyenvantan", email="nguyenvantan@gmail.com",
                            password=make_password(os.getenv('DEFAULT_STAFF_PASSWORD')),
                            role=staff_role),
              account_model(is_superuser=False, first_name="Ho", last_name="Van Y", is_staff=True,
                            username="hovany", email="hovany@gmail.com",
                            password=make_password(os.getenv('DEFAULT_STAFF_PASSWORD')),
                            role=staff_role),
              account_model(is_superuser=False, first_name="Tran", last_name="Thi Thu Trang", is_staff=True,
                            username="tranthithutrang", email="tranthithutrang@gmail.com",
                            password=make_password(os.getenv('DEFAULT_STAFF_PASSWORD')),
                            role=staff_role),
              account_model(is_superuser=False, first_name="Nguyen", last_name="Thi Tuyet", is_staff=True,
                            username="nguyenthituyet", email="nguyenthituyet@gmail.com",
                            password=make_password(os.getenv('DEFAULT_STAFF_PASSWORD')),
                            role=staff_role),
              account_model(is_superuser=False, first_name="Tran", last_name="Thanh Tu", is_staff=True,
                            username="tranthanhtu", email="tranthanhtu@gmail.com",
                            password=make_password(os.getenv('DEFAULT_STAFF_PASSWORD')),
                            role=staff_role),
              account_model(is_superuser=False, first_name="Vuong", last_name="Bao Nhac", is_staff=True,
                            username="vuongbaonhac", email="vuongbaonhac@gmail.com",
                            password=make_password(os.getenv('DEFAULT_STAFF_PASSWORD')),
                            role=staff_role)
              ])

    account_model.objects.bulk_create(staffs)


class Migration(migrations.Migration):
    dependencies = [
        ('api_account', '0004_migrate_user'),
    ]

    operations = [
        migrations.RunPython(initial_data)
    ]

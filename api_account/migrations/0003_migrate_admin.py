# Generated by Django 3.2.8 on 2021-12-19 15:46
from django.contrib.auth.hashers import make_password
from django.db import migrations
from dotenv import load_dotenv
import os

load_dotenv()


def initial_admin_data(apps, schema_editor):
    account_model = apps.get_model("api_account", "Account")
    role_model = apps.get_model("api_account", "Role")

    admin_role = role_model.objects.filter(name="ADMIN").first()

    admin = account_model(is_superuser=True, first_name="Super", last_name="Admin", is_staff=True, username="admin",
                          email="contact.kob.sgroup@gmail.com",
                          password=make_password(os.getenv('DEFAULT_ADMIN_PASSWORD')),
                          role=admin_role)

    admin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api_account', '0002_migrate_roles'),
    ]

    operations = [
        migrations.RunPython(initial_admin_data, migrations.RunPython.noop)
    ]

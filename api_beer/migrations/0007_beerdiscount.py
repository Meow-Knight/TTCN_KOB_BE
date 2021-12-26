# Generated by Django 3.2.8 on 2021-12-25 15:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api_beer', '0006_auto_20211220_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeerDiscount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_activate', models.BooleanField(default=True)),
                ('discount_percent', models.IntegerField()),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_beer.beer')),
            ],
            options={
                'db_table': 'beer_discount',
                'ordering': ('name',),
            },
        ),
    ]
# Generated by Django 3.2.8 on 2022-01-07 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_beer', '0005_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'order_status',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_price', models.IntegerField()),
                ('total_discount', models.IntegerField()),
                ('shipping_address', models.CharField(max_length=200)),
                ('shipping_phone', models.CharField(max_length=20)),
                ('done_at', models.DateTimeField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
                ('order_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_order.orderstatus')),
            ],
            options={
                'db_table': 'order',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_detail', to='api_beer.beer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_detail', to='api_order.order')),
            ],
            options={
                'db_table': 'order_detail',
                'ordering': ('-created_at',),
                'unique_together': {('beer', 'order')},
            },
        ),
    ]

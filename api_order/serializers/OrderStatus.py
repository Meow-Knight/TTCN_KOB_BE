from rest_framework import serializers

from api_order.models import OrderStatus


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class RetrieveOrderStatus(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['name']
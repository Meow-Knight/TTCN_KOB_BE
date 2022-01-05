from rest_framework import serializers

from api_order.models import Order, OrderStatus, OrderDetail
from api_order.serializers import OrderDetailSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1


class CUOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id']


class RetrieveOrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(RetrieveOrderSerializer, self).to_representation(instance)
        order_status = OrderStatus.objects.get(pk=data.get('order_status'))
        data['order_status'] = order_status.name
        order_detail = OrderDetail.objects.filter(order=data.get('id'))
        data['order_detail'] = list(OrderDetailSerializer(order_detail, many=True).data)
        return data

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'total_discount', 'shipping_address', 'shipping_phone', 'order_status']

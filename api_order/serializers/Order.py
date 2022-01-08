from rest_framework import serializers

from api_account.models import Account
from api_order.models import Order, OrderStatus, OrderDetail
from api_order.serializers import OrderDetailSerializer, ListOrderDetailSerializer


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


class ListOrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(ListOrderSerializer, self).to_representation(instance)
        order_status = OrderStatus.objects.get(pk=data.get('order_status'))
        data['order_status'] = order_status.name
        return data

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'total_discount', 'shipping_address', 'shipping_phone', 'done_at', 'order_status']


class RetrieveOrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(RetrieveOrderSerializer, self).to_representation(instance)
        order_status = OrderStatus.objects.get(pk=data.get('order_status'))
        data['order_status'] = order_status.name

        # chỗ này thêm giúp t cái progress với
        data['progress'] = []

        order_detail = OrderDetail.objects.filter(order=data.get('id'))
        data['order_detail'] = list(ListOrderDetailSerializer(order_detail, many=True).data)

        account = Account.objects.filter(pk=data['account'])
        if account.exists():
            account = account.first()
            data['account'] = {"id": account.id, "username": account.username}

        return data

    class Meta:
        model = Order
        fields = "__all__"

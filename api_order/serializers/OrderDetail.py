from rest_framework import serializers

from api_beer.serializers import ItemBeerSerializer
from api_order.models import OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    beer = ItemBeerSerializer()

    class Meta:
        model = OrderDetail
        fields = ['id', 'amount', 'beer']


class CUOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = '__all__'

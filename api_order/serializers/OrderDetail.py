from rest_framework import serializers

from api_beer.models import Beer
from api_beer.serializers import ItemBeerSerializer, BeerOrderDetailSerializer
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


class ListOrderDetailSerializer(serializers.ModelSerializer):
    beer = BeerOrderDetailSerializer()

    def to_representation(self, instance):
        data = super(ListOrderDetailSerializer, self).to_representation(instance)
        beer = data['beer']
        if beer.get('discount_percent') is not None:
            data['total_price'] = beer['new_price'] * data['amount']
        else:
            data['total_price'] = beer['price'] * data['amount']

        return data

    class Meta:
        model = OrderDetail
        fields = ['id', 'amount', 'beer']

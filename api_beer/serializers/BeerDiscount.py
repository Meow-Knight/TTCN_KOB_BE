from rest_framework import serializers

from api_beer.models import BeerDiscount


class BeerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerDiscount
        fields = '__all__'


class SimplestBeerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerDiscount
        fields = ('id', 'discount_percent', 'beer')

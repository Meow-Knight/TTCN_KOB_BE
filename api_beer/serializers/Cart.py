from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api_beer.models import Cart, Beer
from api_beer.serializers import ItemBeerSerializer


class CUCartSerializer(serializers.ModelSerializer):

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Amount must positive number")
        return value

    class Meta:
        model = Cart
        fields = '__all__'


class BeerDetailCartSerializer(serializers.ModelSerializer):
    beer = ItemBeerSerializer()

    class Meta:
        model = Cart
        fields = ('id', 'amount', 'beer',)


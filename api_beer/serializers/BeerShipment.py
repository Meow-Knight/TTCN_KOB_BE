from rest_framework import serializers

from api_beer.models import BeerShipment


class BeerShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerShipment
        fields = '__all__'


class ListBeerShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerShipment
        fields = '__all__'
        depth = 1

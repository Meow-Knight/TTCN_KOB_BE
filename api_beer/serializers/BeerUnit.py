from rest_framework import serializers

from api_beer.models import BeerUnit


class BeerUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerUnit
        fields = '__all__'

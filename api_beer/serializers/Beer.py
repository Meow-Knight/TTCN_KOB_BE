from rest_framework import serializers

from api_beer.models import Beer


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'


class ListBeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'
        depth = 1

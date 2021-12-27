from rest_framework import serializers
from django.db import models
from api_beer.models import Beer, BeerPhoto


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'


class ListBeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'
        depth = 1


class BeerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'
        depth = 1
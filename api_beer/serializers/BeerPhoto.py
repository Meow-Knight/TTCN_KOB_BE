from rest_framework import serializers

from api_beer.models import BeerPhoto


class BeerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerPhoto
        fields = '__all__'

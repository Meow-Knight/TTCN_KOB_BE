from rest_framework import serializers

from api_beer.models import BeerPhoto


class CUBeerPhotoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = BeerPhoto
        fields = ('id', 'beer', )


class BeerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerPhoto
        fields = ('id', 'beer', 'link',)

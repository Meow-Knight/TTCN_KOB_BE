from rest_framework import serializers

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


class RetrieveBeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super(RetrieveBeerSerializer, self).to_representation(instance)
        beer_id = data['id']
        photos = BeerPhoto.objects.filter(beer_id=beer_id).values("link")
        if photos:
            data["photos"] = list(photos)
        return data

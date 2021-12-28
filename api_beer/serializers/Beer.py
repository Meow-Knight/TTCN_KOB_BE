import datetime
from rest_framework import serializers
from django.db import models
from api_beer.models import Beer, BeerPhoto, BeerDiscount


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'


class ListBeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'
        depth = 1


# class BeerDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Beer
#         fields = '__all__'
#         depth = 1

class SameProducerBeerSerializer(serializers.ModelSerializer):
    class Meta:
        models = Beer
        fields = ('id', 'name', 'capacity', 'price',)


class DetailBeerSerializer(serializers.ModelSerializer):
    """
    This serializer contains beer record include extend fields:
    - First photo
    - Available sale discount
    """

    def to_representation(self, instance):
        data = super(DetailBeerSerializer, self).to_representation(instance)
        beer_id = data['id']
        photos = BeerPhoto.objects.filter(beer_id=beer_id)
        if photos.exists():
            data['photo'] = photos.first().link
        discount = BeerDiscount.objects.filter(beer_id=beer_id,
                                               discount__start_date__lte=datetime.date.today(),
                                               discount__end_date__gte=datetime.date.today(),
                                               discount__is_activate=True).values("discount_percent")
        if discount.exists():
            discount = discount.first()
            data.update(discount)

        return data

    class Meta:
        model = Beer
        fields = ('id', 'name', 'capacity', 'price',)
        depth = 1
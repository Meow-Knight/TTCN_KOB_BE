import datetime

from rest_framework import serializers

from api_beer.models import Beer, BeerPhoto, BeerDiscount
from api_beer.serializers import BeerPhotoSerializer


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
        photos = BeerPhoto.objects.filter(beer_id=beer_id)
        photo_serializer = BeerPhotoSerializer(photos, many=True)
        if photos:
            data["photos"] = photo_serializer.data
        return data


class ItemBeerSerializer(serializers.ModelSerializer):
    """
    This serializer contains beer record include extend fields:
    - First photo
    - Available sale discount
    """

    def to_representation(self, instance):
        data = super(ItemBeerSerializer, self).to_representation(instance)
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


class SearchItemBeerSerializer(serializers.ModelSerializer):
    """
    This serializer contains beer record include extend fields:
    - First photo
    - Available sale discount
    """

    def to_representation(self, instance):
        data = super(SearchItemBeerSerializer, self).to_representation(instance)
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
        fields = ('id', 'name', 'capacity', 'price', 'alcohol_concentration', 'producer')
        depth = 1

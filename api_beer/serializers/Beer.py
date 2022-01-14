import datetime

from rest_framework import serializers, fields

from api_beer.models import Beer, BeerPhoto, BeerDiscount
from api_beer.serializers import BeerPhotoSerializer
from api_order.models import OrderDetail


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'


class ListBeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'
        depth = 1


class DropdownBeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = ('id', 'name',)


class TopBeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = ('id', 'total_sum', "name")

    def build_unknown_field(self, field_name, model_class):
        """
        Return a two tuple of (cls, kwargs) to build a serializer field with. For fields that werent originally on
        The model
        """
        return fields.CharField, {'read_only': True}

    def to_representation(self, instance):
        data = super(TopBeerSerializer, self).to_representation(instance)
        beer_id = data['id']
        photos = BeerPhoto.objects.filter(beer_id=beer_id)
        if photos.exists():
            data['photo'] = photos.first().link
        return data


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


class BeerOrderDetailSerializer(serializers.ModelSerializer):
    """
    This serializer contains beer record include extend fields:
    - First photo
    - Available sale discount
    """

    def to_representation(self, instance):
        data = super(BeerOrderDetailSerializer, self).to_representation(instance)
        beer_id = data['id']
        photos = BeerPhoto.objects.filter(beer_id=beer_id)
        if photos.exists():
            data['photo'] = photos.first().link

        order_detail = OrderDetail.objects.filter(beer=beer_id)
        if order_detail.exists():
            order_detail = order_detail.first()
            discount = BeerDiscount.objects.filter(beer_id=beer_id,
                                                   discount__start_date__lte=order_detail.created_at,
                                                   discount__end_date__gte=order_detail.created_at,
                                                   discount__is_activate=True).values("discount_percent")
            if discount.exists():
                discount = discount.first()
                data.update(discount)
                data['new_price'] = data['price'] - data['price'] * data['discount_percent'] / 100

        return data

    class Meta:
        model = Beer
        fields = ('id', 'name', 'capacity', 'price',)
        depth = 1
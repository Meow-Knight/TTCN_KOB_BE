from rest_framework import serializers

from api_beer.models import Discount, Beer
from api_beer.serializers import ItemBeerSerializer, SimplestBeerDiscountSerializer


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError("Invalid start_date, end_date")
        return attrs


class DetailDiscountSerializer(serializers.ModelSerializer):
    beer_discounts = SimplestBeerDiscountSerializer(source='beer_discount', many=True)

    class Meta:
        model = Discount
        fields = '__all__'


class DiscountWithItemBeerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(DiscountWithItemBeerSerializer, self).to_representation(instance)
        discount_id = data['id']
        beers = Beer.objects.filter(beer_discount__discount_id=discount_id)
        if beers.exists():
            item_beer_serializer = ItemBeerSerializer(beers, many=True)
            data['beers'] = item_beer_serializer.data
        return data

    class Meta:
        model = Discount
        fields = ('id', 'name', 'start_date', 'end_date')

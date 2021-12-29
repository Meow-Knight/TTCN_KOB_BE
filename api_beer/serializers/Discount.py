from rest_framework import serializers

from api_beer.models import Discount, Beer
from api_beer.serializers import ItemBeerSerializer


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

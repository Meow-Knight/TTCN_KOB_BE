import random

from django.db import transaction

from api_beer.models import BeerPhoto, Beer, Discount
from api_beer.serializers import ItemBeerSerializer, DiscountWithItemBeerSerializer
from api_beer.services import BeerPhotoService


class BeerService:

    @classmethod
    @transaction.atomic
    def create_beer_with_photos(cls, beer_serializer, images):
        beer = beer_serializer.save()
        beer_photos = []
        links = BeerPhotoService.upload_images(images)
        for link in links:
            beer_photos.append(BeerPhoto(link=link, beer=beer))
        BeerPhoto.objects.bulk_create(beer_photos)

    @classmethod
    def get_random_beers(cls, amount):
        all_records = list(Beer.objects.values_list('id', flat=True))
        random_records = random.sample(all_records, min(len(all_records), amount))
        return Beer.objects.filter(id__in=random_records)

    @classmethod
    def get_homepage_data(cls, random_amount):
        random_query_set = BeerService.get_random_beers(random_amount)
        random_serializer = ItemBeerSerializer(random_query_set, many=True)
        discount_query_set = Discount.objects.all()
        discount_serializer = DiscountWithItemBeerSerializer(discount_query_set, many=True)

        return {'randoms': random_serializer.data, 'discounts': discount_serializer.data}

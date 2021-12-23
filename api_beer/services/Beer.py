from django.db import transaction

from api_beer.models import BeerPhoto

import cloudinary
import cloudinary.uploader
import cloudinary.api


class BeerService:

    @classmethod
    @transaction.atomic
    def create_beer_with_photos(cls, beer_serializer, images):
        beer = beer_serializer.save()
        beer_photos = []
        for image in images:
            upload_data = cloudinary.uploader.upload(image, folder="sgroup/kob/beers/")
            beer_photos.append(BeerPhoto(link=upload_data.get("url"), beer=beer))
        BeerPhoto.objects.bulk_create(beer_photos)

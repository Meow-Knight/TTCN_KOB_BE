import os

from django.db import transaction
from dotenv import load_dotenv

from api_base.services import CloudinaryService
from api_beer.models import BeerPhoto, Beer

load_dotenv()


class BeerPhotoService:

    @classmethod
    def upload_images(cls, images):
        links = []
        for image in images:
            upload_data = CloudinaryService.upload_beer_image(image)
            links.append(upload_data.get("url"))

        return links

    @classmethod
    @transaction.atomic
    def create_beer_photos(cls, beer_id, images):
        beer = Beer.objects.get(id=beer_id)
        links = cls.upload_images(images)
        beer_photos = []
        for link in links:
            beer_photos.append(BeerPhoto(link=link, beer=beer))
        BeerPhoto.objects.bulk_create(beer_photos)
        return links

    @classmethod
    def delete_images(cls, link):
        pub_id = cls.get_public_id(link)
        res = CloudinaryService.delete_image(pub_id)
        if res['result'] == "ok":
            return True
        return False

    @classmethod
    def get_public_id(cls, link):
        image_name = link.split("/")[-1].split(".")[0]
        return os.getenv("CLOUDINARY_BEER_PHOTO_FOLDER") + image_name

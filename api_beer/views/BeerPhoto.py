from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_beer.models import BeerPhoto
from api_beer.serializers import BeerPhotoSerializer, CUBeerPhotoSerializer
from api_beer.services import BeerPhotoService


class BeerPhotoViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BeerPhotoSerializer
    queryset = BeerPhoto.objects.all()

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist("images")

        if not images:
            return Response({"details": "Images field is empty"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CUBeerPhotoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            links = BeerPhotoService.create_beer_photos(serializer.data['beer'], images)
            res = serializer.data
            res['links'] = links
            return Response({"details": res}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new beer record"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        beer_photo = self.get_object()
        if BeerPhotoService.delete_images(beer_photo.link):
            beer_photo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"details": "Cannot delete this record"}, status=status.HTTP_400_BAD_REQUEST)

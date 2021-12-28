from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_beer.serializers import BeerPhotoSerializer
from api_beer.models import BeerPhoto
from api_base.views import BaseViewSet


class BeerPhotoViewSet(BaseViewSet):
    serializer_class = BeerPhotoSerializer
    queryset = BeerPhoto.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new beer photo record"}, status=status.HTTP_400_BAD_REQUEST)


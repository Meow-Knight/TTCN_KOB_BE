from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_beer.serializers import BeerSerializer, ListBeerSerializer, BeerPhotoSerializer
from api_beer.models import Beer, BeerPhoto
from api_beer.serializers.Beer import BeerDetailSerializer
from api_beer.services import BeerService
from api_base.views import BaseViewSet


class BeerViewSet(BaseViewSet):
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    serializer_map = {
        "list": ListBeerSerializer
    }

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist("images")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            BeerService.create_beer_with_photos(serializer, images)
            return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new beer record"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        query_set = Beer.objects
        search_query = request.query_params.get("q", "")
        query_set = query_set.filter(name__icontains=search_query)
        sort_query = request.query_params.get("sort")
        if sort_query:
            try:
                if sort_query.startswith("-"):
                    Beer._meta.get_field(sort_query[1:])
                else:
                    Beer._meta.get_field(sort_query)
                query_set = query_set.order_by(sort_query)
            except:
                pass

        self.queryset = query_set
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def info(self, request, *args, **kwargs):
        # fetch : infor beer + load image of each beer
        # fetch : a list about beers that relate with upon beer
        beer = BeerDetailSerializer(self.get_object())
        photo = BeerPhoto.objects.filter(beer=self.get_object())
        # select * from Beer where Beer.origin_nation = beer.origin_nation
        # select * from Beer
        # select * from Beer
        if photo.exists():
            photo = BeerPhotoSerializer(photo.first())
            return Response({"detail": beer.data, "photo": photo.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"details": "Cannot get beer detail information"}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api_beer.serializers import BeerSerializer, ListBeerSerializer, BeerPhotoSerializer
from api_beer.models import Beer, BeerPhoto
from api_beer.serializers.Beer import BeerDetailSerializer
from api_beer.services import BeerService
from api_base.views import BaseViewSet


class BeerViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    serializer_map = {
        "list": ListBeerSerializer,
        "retrieve": ListBeerSerializer,
    }
    permission_map = {
        "list": [IsAuthenticated]
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
    def info(self, request, pk, *args, **kwargs):
        beer = Beer.objects.get(pk=pk)
        #photo = BeerPhoto.objects.filter(beer=beer.id)
        beer_producer = Beer.objects.filter(producer=beer.producer)
        if beer:
            beer = BeerDetailSerializer(beer)
            beer_producer = ListBeerSerializer(beer_producer, many=True)
            #photo = BeerPhotoSerializer(photo.first())
            return Response({"detail": beer.data, "beer_nation": beer_producer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"details": "Cannot get beer detail information"}, status=status.HTTP_400_BAD_REQUEST)

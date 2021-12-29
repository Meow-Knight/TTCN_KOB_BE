from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api_beer.models import BeerPhoto
from api_beer.serializers import BeerSerializer, ListBeerSerializer, RetrieveBeerSerializer, ItemBeerSerializer, BeerPhotoSerializer, BeerDetailSerializer
from api_beer.models import Beer
from api_beer.services import BeerService
from api_base.views import BaseViewSet


class BeerViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    permission_map = {
        "list": [],
        "retrieve": [],
        "info": []
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
        beer = self.get_object()
        photos = BeerPhoto.objects.filter(beer=beer.id).values('link')
        same_producer_beers = Beer.objects.filter(producer=beer.producer).exclude(id=beer.id)
        #beer = ListBeerSerializer(beer)
        beer = BeerDetailSerializer(beer)
        beer_producer_serializer = ItemBeerSerializer(same_producer_beers, many=True)
        res_data = {"details": beer.data}
        if photos.exists():
            res_data['photos'] = map(lambda photo: photo['link'], list(photos))
        if same_producer_beers.exists():
            res_data['same_producer_beers'] = beer_producer_serializer.data
        return Response(res_data, status=status.HTTP_200_OK)

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_beer.models import Beer, BeerPhoto
from api_beer.serializers import BeerSerializer, ListBeerSerializer, RetrieveBeerSerializer, ItemBeerSerializer, \
    SearchItemBeerSerializer, DropdownBeerSerializer
from api_beer.services import BeerService
from api_beer.constants import SaleDurationEnum, SaleType
from api_account.permissions import StaffOrAdminPermission, AdminPermission


class BeerViewSet(BaseViewSet):
    permission_classes = [StaffOrAdminPermission]
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    serializer_map = {
        "list": ListBeerSerializer,
        "retrieve": RetrieveBeerSerializer,
    }

    permission_map = {
        "list": [],
        "retrieve": [],
        "homepage": [],
        "info": [],
        "user_search": [],
        "get_all_with_name": [],
        "top": [AdminPermission],
        "chart_data": [],
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

    @action(detail=False, methods=['get'])
    def homepage(self, request, *args, **kwargs):
        random_amount = int(request.query_params.get("random_amount", "4"))
        response_data = BeerService.get_homepage_data(random_amount)
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def info(self, request, pk, *args, **kwargs):
        beer = self.get_object()
        photos = BeerPhoto.objects.filter(beer=beer.id).values('link')
        same_producer_beers = Beer.objects.filter(producer=beer.producer).exclude(id=beer.id)
        beer = ListBeerSerializer(beer)
        beer_producer_serializer = ItemBeerSerializer(same_producer_beers, many=True)
        res_data = {"details": beer.data}
        if photos.exists():
            res_data['photos'] = map(lambda photo: photo['link'], list(photos))
        if same_producer_beers.exists():
            res_data['same_producer_beers'] = beer_producer_serializer.data
        return Response(res_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def user_search(self, request, *args, **kwargs):
        query_set = Beer.objects
        search_query = request.query_params.get("q", "").strip()
        if search_query:
            q = Q(name__icontains=search_query) | Q(producer__name__icontains=search_query)
            query_set = query_set.filter(q)
        serializer = SearchItemBeerSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_all_with_name(self, request, *args, **kwargs):
        return Response(DropdownBeerSerializer(self.get_queryset(), many=True).data)

    @action(detail=False, methods=['get'])
    def top(self, request, *args, **kwargs):
        amount = request.query_params.get("amount")
        duration = request.query_params.get("duration")
        type = request.query_params.get("type")
        enum_type = SaleType.get_by_value(type)
        if not enum_type:
            enum_type = SaleType.AMOUNT
        enum_duration = SaleDurationEnum.get_by_value(duration)
        try:
            amount = int(amount)
        except Exception:
            amount = 5

        return Response(BeerService.get_top_beers(amount, enum_duration, enum_type), status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def chart_data(self, request, *args, **kwargs):
        duration = request.query_params.get("duration")
        type = request.query_params.get("type")
        enum_duration = SaleDurationEnum.get_by_value(duration)
        enum_type = SaleType.get_by_value(type)
        if not enum_type:
            enum_type = SaleType.AMOUNT

        chart_data = BeerService.get_chart_data(enum_duration, enum_type)
        response = BeerService.format_chart_data(chart_data, enum_duration)
        return Response(response, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def sales_statistics(self, request, *args, **kwargs):
        res_data = BeerService.get_sales_statistics(request)
        return Response(res_data, status=status.HTTP_200_OK)
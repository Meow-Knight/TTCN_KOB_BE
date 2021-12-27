from api_beer.serializers import BeerShipmentSerializer, ListBeerShipmentSerializer
from api_beer.models import BeerShipment
from api_base.views import BaseViewSet
from rest_framework.response import Response


class BeerShipmentViewSet(BaseViewSet):
    serializer_class = BeerShipmentSerializer
    queryset = BeerShipment.objects.all()
    serializer_map = {
        "list": ListBeerShipmentSerializer,
        "retrieve": ListBeerShipmentSerializer
    }

    # pagination_class =
    # def list(self, request, *args, **kwargs):
    #     s = request.GET.get('s')
    #     sort = request.GET.get('sort')
    #     beer_shipment = BeerShipment.objects.all()
    #
    #     if s:
    #         beer_shipment = BeerShipment.objects.filter(beer__name__icontains=s)
    #     if sort == 'asc':
    #         beer_shipment = BeerShipment.objects.order_by('shipment_date')
    #     elif sort == 'desc':
    #         beer_shipment = BeerShipment.objects.order_by('-shipment_date')
    #
    #     serializer = BeerShipmentSerializer(beer_shipment, many=True)
    #     return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        query_set = BeerShipment.objects
        search_query = request.query_params.get("q", "")
        query_set = query_set.filter(beer__name__icontains=search_query)
        sort_query = request.query_params.get("sort")
        if sort_query:
            try:
                if sort_query.startswith("-"):
                    BeerShipment._meta.get_field(sort_query[1:])
                else:
                    BeerShipment._meta.get_field(sort_query)
                query_set = query_set.order_by(sort_query)

            except:
                pass

        self.queryset = query_set
        return super().list(request, *args, **kwargs)

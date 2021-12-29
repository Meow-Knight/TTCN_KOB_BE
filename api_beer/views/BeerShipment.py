from api_beer.serializers import BeerShipmentSerializer, ListBeerShipmentSerializer
from api_beer.models import BeerShipment
from api_base.views import BaseViewSet


class BeerShipmentViewSet(BaseViewSet):
    serializer_class = BeerShipmentSerializer
    queryset = BeerShipment.objects.all()
    serializer_map = {
        "list": ListBeerShipmentSerializer,
        "retrieve": ListBeerShipmentSerializer
    }

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

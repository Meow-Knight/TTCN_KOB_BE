from rest_framework import viewsets

from api_beer.serializers import BeerUnitSerializer
from api_beer.models import BeerUnit


class BeerUnitViewSet(viewsets.ModelViewSet):
    serializer_class = BeerUnitSerializer
    queryset = BeerUnit.objects.all()

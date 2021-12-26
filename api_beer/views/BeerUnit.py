from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api_beer.serializers import BeerUnitSerializer
from api_beer.models import BeerUnit


class BeerUnitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BeerUnitSerializer
    queryset = BeerUnit.objects.all()

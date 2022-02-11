from rest_framework.permissions import IsAdminUser

from api_beer.serializers import BeerUnitSerializer
from api_beer.models import BeerUnit
from api_base.views import BaseViewSet


class BeerUnitViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BeerUnitSerializer
    queryset = BeerUnit.objects.all()
    permission_map = {
        "list": [],
        "retrieve": []
    }

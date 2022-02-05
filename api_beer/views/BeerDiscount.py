from api_account.permissions import AdminPermission
from api_base.views import BaseViewSet
from api_beer.models import BeerDiscount
from api_beer.serializers import BeerDiscountSerializer


class BeerDiscountViewSet(BaseViewSet):
    permission_classes = [AdminPermission]
    serializer_class = BeerDiscountSerializer
    queryset = BeerDiscount.objects.all()

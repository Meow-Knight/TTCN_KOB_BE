from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_beer.models import Cart
from api_beer.serializers import CUCartSerializer, BeerDetailCartSerializer


class CartViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CUCartSerializer
    queryset = Cart.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(account=user)
        serializer = BeerDetailCartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        account = request.user
        request.data['account'] = account.id
        return super().create(request)

    def update(self, request, *args, **kwargs):
        account = request.user
        request.data['account'] = account.id
        return super().update(request)

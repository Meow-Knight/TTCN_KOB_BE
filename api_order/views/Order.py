from datetime import date

from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.serializers import GeneralInfoAccountSerializer
from api_base.views import BaseViewSet
from api_beer.models import Cart, Beer, Discount
from api_beer.serializers import BeerDetailCartSerializer
from api_order.models import Order, OrderStatus
from api_order.serializers import OrderSerializer, CUOrderSerializer
from api_order.services import OrderService


class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        carts = request.data['carts']
        if OrderService.check_amount_order(carts) is False:
            return Response({'detail': 'Sorry. There are not enough items in stock to fulfill your order'},
                            status=status.HTTP_400_BAD_REQUEST)

        order_status = OrderStatus.objects.get(name='PENDING')
        request.data['order_status'] = order_status.id
        request.data['account'] = request.user.id
        ser = CUOrderSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            res = OrderService.create_order_and_order_detail(ser, carts)
            return Response(res, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def checkout(self, request):
        try:
            user = request.user
            carts = Cart.objects.filter(account=user.id)
        except:
            carts = []

        total_price = 0.0
        total_discount = 0.0
        for cart in carts:
            price = cart.beer.price
            total_discount = total_discount + price * cart.amount
            beer_discount = Beer.objects.get(pk=cart.beer_id).beer_discount.get()
            if beer_discount:
                discount = Discount.objects.get(pk=beer_discount.discount_id)
                if discount.end_date > date.today():
                    price = cart.beer.price - cart.beer.price * beer_discount.discount_percent / 100
            total_price = total_price + price * cart.amount
        total_discount = total_discount - total_price
        user = GeneralInfoAccountSerializer(user)
        res_carts = BeerDetailCartSerializer(carts, many=True)
        res_data = {'user': user.data,
                    'carts': list(res_carts.data),
                    'total_price': total_price,
                    'total_discount': total_discount}
        return Response(res_data, status=status.HTTP_200_OK)

from django.db import transaction
from django.db.models import Sum

from api_beer.models import Beer
from api_order.serializers import CUOrderDetailSerializer


class OrderService:

    @classmethod
    def check_amount_order(cls, carts):
        for cart in carts:
            b = Beer.objects.get(pk=cart.get('beer'))
            order_detail = b.order_detail.all().aggregate(Sum('amount'))
            beer_shipment = b.beer_shipment.all().aggregate(Sum('amount'))
            if cart.get('amount') + order_detail.get('amount__sum') > beer_shipment.get('amount__sum'):
                return False

        return True

    @classmethod
    @transaction.atomic
    def create_order_and_order_detail(cls, ser, carts):
        order = ser.save()
        res = ser.data
        for cart in carts:
            cart['order'] = order.id
        order_detail_ser = CUOrderDetailSerializer(data=carts, many=True)
        if order_detail_ser.is_valid(raise_exception=True):
            order_details = order_detail_ser.save()
            res['order_details'] = order_detail_ser.data
        return res

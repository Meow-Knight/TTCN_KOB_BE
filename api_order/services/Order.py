from django.db import transaction
from django.db.models import Sum

from api_beer.models import Beer, Cart
from api_order.serializers import CUOrderDetailSerializer, ProgressSerializer, RetrieveProgressSerializer


class OrderService:

    @classmethod
    @transaction.atomic
    def check_amount_order(cls, carts):
        for cart in carts:
            b = Beer.objects.get(pk=cart.get('beer'))
            order_detail = b.order_detail.all().aggregate(Sum('amount'))
            if order_detail.get('amount__sum') is None:
                order_detail = 0
            else:
                order_detail = order_detail.get('amount__sum')

            beer_shipment = b.beer_shipment.all().aggregate(Sum('amount'))
            if beer_shipment.get('amount__sum') is None:
                return False
            else:
                beer_shipment = beer_shipment.get('amount__sum')

            if cart.get('amount') + order_detail > beer_shipment:
                return False

        return True

    @classmethod
    @transaction.atomic
    def delete_cart(cls, carts, request):
        beer_ids = []
        for item in carts:
            beer_ids.append(item['beer'])
        Cart.objects.filter(account=request.user, beer_id__in=beer_ids).delete()

    @classmethod
    @transaction.atomic
    def create_order_and_order_detail(cls, ser, carts, request, order_status):
        order = ser.save()
        res = ser.data
        progress = {"order_status": order_status.id, "order": order.id}
        progress = ProgressSerializer(data=progress)
        if progress.is_valid(raise_exception=True):
            progress = progress.save()
            res['progress'] = RetrieveProgressSerializer(progress).data

        for cart in carts:
            cart['order'] = order.id
        order_detail_ser = CUOrderDetailSerializer(data=carts, many=True)
        if order_detail_ser.is_valid(raise_exception=True):
            order_details = order_detail_ser.save()
            cls.delete_cart(carts, request)
            res['order_details'] = order_detail_ser.data
        return res

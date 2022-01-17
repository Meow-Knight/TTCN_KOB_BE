from django.db import transaction
from django.db.models import Sum

from api_beer.models import Beer, Cart
from api_order import constants
from api_account.constants.Data import RoleData
from api_order.models import OrderStatus
from api_order.serializers import CUOrderDetailSerializer, ProgressSerializer, RetrieveProgressSerializer


class OrderService:

    @classmethod
    @transaction.atomic
    def auto_completed_order(cls, orders):
        if orders.exists():
            res = []
            role = RoleData.CUSTOMER.value.get("name")
            key_change = constants.OrderStatus.COMPLETED.value.get("name")
            for order in orders:
                res_item = cls.change_order_status(order, key_change, role)
                if res_item is not None:
                    res.append(res_item)
            return res

    @classmethod
    @transaction.atomic
    def add_progress_order(cls, order, order_status):
        progress = {"order_status": order_status.id, "order": order.id}
        progress = ProgressSerializer(data=progress)
        if progress.is_valid(raise_exception=True):
            progress.save()

    @classmethod
    @transaction.atomic
    def my_switcher(cls, key_change, order_status, role):
        if constants.OrderStatus.CONFIRMED.value.get("name") == key_change and role != RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.PENDING.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.CONFIRMED.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.DELIVERING.value.get("name") == key_change and role != RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.CONFIRMED.value.get("name") \
                    or order_status == constants.OrderStatus.NOTRECEIVED.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.DELIVERING.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.DELIVERED.value.get("name") == key_change and role != RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.DELIVERING.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.DELIVERED.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.COMPLETED.value.get("name") == key_change and role == RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.DELIVERED.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.COMPLETED.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.NOTRECEIVED.value.get("name") == key_change and role == RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.DELIVERED.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.NOTRECEIVED.value.get("name"))
                if new_status.exists():
                    return new_status.first()

    @classmethod
    @transaction.atomic
    def change_order_status(cls, order, key_change, role):
        res = {"success": False, "id": order.id}
        order_status = order.order_status.name
        new_status = cls.my_switcher(key_change, order_status, role)
        if new_status is not None:
            order.order_status = new_status
            order.save()
            cls.add_progress_order(order, new_status)
            res['success'] = True
        return res

    @classmethod
    @transaction.atomic
    def cancel_order(cls, order):
        if order.exists():
            order = order.first()
            res = {"success": False, "id": order.id}
            order_status = order.order_status.name
            if constants.OrderStatus.PENDING.value.get('name') == order_status:
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.CANCELED.value.get('name'))
                if new_status.exists():
                    order.order_status = new_status.first()
                    order.save()
                    cls.add_progress_order(order, new_status.first())
                    res['success'] = True
            return res

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


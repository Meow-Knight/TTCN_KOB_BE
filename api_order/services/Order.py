import datetime

from django.db import transaction
from django.db.models import Sum

from api_account.serializers import GeneralInfoAccountSerializer
from api_base.services import CurrencyConvertor
from api_beer.models import Beer, Cart, BeerDiscount
from api_beer.serializers import BeerDetailCartSerializer
from api_order import constants
from api_account.constants.Data import RoleData
from api_order.constants import Data
from api_order.models import OrderStatus, PaymentMethod
from api_order.serializers import CUOrderDetailSerializer, ProgressSerializer, RetrieveProgressSerializer
from api_order.serializers.Payment import PaymentSerializer


class OrderService:

    @classmethod
    @transaction.atomic
    def auto_completed_order(cls, orders, request):
        if orders.exists():
            res = []
            role = RoleData.CUSTOMER.value.get("name")
            key_change = constants.OrderStatus.COMPLETED.value.get("name")
            for order in orders:
                res_item = cls.change_order_status(order, key_change, role, request)
                if res_item is not None:
                    res.append(res_item)
            return res

    @classmethod
    @transaction.atomic
    def add_progress_order(cls, order, order_status, request):
        progress = {"order_status": order_status.id, "order": order.id, "account": request.user.id}
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
    def change_order_status(cls, order, key_change, role, request):
        res = {"success": False, "id": order.id}
        order_status = order.order_status.name
        new_status = cls.my_switcher(key_change, order_status, role)
        if new_status is not None:
            order.order_status = new_status
            order.save()
            cls.add_progress_order(order, new_status, request)
            res['success'] = True
        return res

    @classmethod
    @transaction.atomic
    def cancel_order(cls, order, request):
        if order.exists():
            order = order.first()
            res = {"success": False, "id": order.id}
            order_status = order.order_status.name
            if constants.OrderStatus.PENDING.value.get('name') == order_status:
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.CANCELED.value.get('name'))
                if new_status.exists():
                    order.order_status = new_status.first()
                    order.save()
                    cls.add_progress_order(order, new_status.first(), request)
                    res['success'] = True
            return res

    @classmethod
    @transaction.atomic
    def check_amount_order(cls, carts):
        beer_ids = []
        cart_error = []
        for cart in carts:
            beer_ids.append(cart.get('beer'))
        beers = Beer.objects.filter(pk__in=beer_ids)
        if beers.exists():
            carts = Cart.objects.filter(beer_id__in=beer_ids)
            if carts.exists():
                for cart in carts:
                    beer = cls.find_beer_by_cart(cart, beers)
                    order_detail = beer.order_detail.all().aggregate(Sum('amount'))
                    if order_detail.get('amount__sum') is None:
                        order_detail = 0
                    else:
                        order_detail = order_detail.get('amount__sum')

                    beer_shipment = beer.beer_shipment.all().aggregate(Sum('amount'))
                    if beer_shipment.get('amount__sum') is None:
                        cart_error.append(cart)
                    else:
                        beer_shipment = beer_shipment.get('amount__sum')

                    if cart.amount + order_detail > beer_shipment:
                        cart_error.append(cart)

            if len(cart_error) > 0:
                carts = BeerDetailCartSerializer(cart_error, many=True)
                return [False, 'Sorry. There are not enough items in stock to fulfill your order', carts.data]
            else:
                return [True]

    @classmethod
    @transaction.atomic
    def delete_cart(cls, carts, request):
        beer_ids = []
        for item in carts:
            beer_ids.append(item['beer'])
        Cart.objects.filter(account=request.user, beer_id__in=beer_ids).delete()

    @classmethod
    @transaction.atomic
    def create_payment(cls, order, request):
        payment_method = PaymentMethod.objects.filter(name=request.data.get('payment_method').upper())
        if payment_method.exists():
            payment_method = payment_method.first()
            payment = {"order": order.id, "payment_method": payment_method.id}
            if payment_method.name == Data.PaymentMethod.PAYPAL.value.get("name"):
                if request.data.get("id_paypal") is not None and request.data.get('email_paypal') is not None:
                    payment['id_paypal'] = request.data['id_paypal']
                    payment['email_paypal'] = request.data['email_paypal']
                else:
                    raise ValueError("Invalid Values")

            payment = PaymentSerializer(data=payment)
            if payment.is_valid(raise_exception=True):
                payment = payment.save()
                return payment
        raise ValueError("Invalid Values")

    @classmethod
    @transaction.atomic
    def create_order_and_order_detail(cls, ser, carts, request, order_status):
        order = ser.save()
        res = ser.data
        progress = {"order_status": order_status.id, "order": order.id, "account": request.user.id}
        progress = ProgressSerializer(data=progress)
        if progress.is_valid(raise_exception=True):
            progress = progress.save()
            res['progress'] = RetrieveProgressSerializer(progress).data

        res_payment = cls.create_payment(order, request)
        if res_payment is not None:
            res['payment_method'] = res_payment.payment_method.name

        for cart in carts:
            cart['order'] = order.id
        order_detail_ser = CUOrderDetailSerializer(data=carts, many=True)
        if order_detail_ser.is_valid(raise_exception=True):
            order_details = order_detail_ser.save()
            cls.delete_cart(carts, request)
            res['order_details'] = order_detail_ser.data
        return res

    @classmethod
    @transaction.atomic
    def find_beer_by_cart(cls, cart, beers):
        for beer in beers:
            if cart.beer.id == beer.id:
                return beer

    @classmethod
    @transaction.atomic
    def find_beer_discount_by_beer(cls, beer, beer_discounts):
        for beer_discount in beer_discounts:
            if beer_discount.beer.id == beer.id:
                return beer_discount

    @classmethod
    @transaction.atomic
    def beer_checkout(cls, user, carts):
        beer_ids = []
        total_price = 0.0
        total_discount = 0.0
        for cart in carts:
            beer_ids.append(cart.beer.id)
        beers = Beer.objects.filter(pk__in=beer_ids)
        if beers.exists():
            beer_discounts = BeerDiscount.objects.filter(beer__in=beer_ids,
                                                         discount__start_date__lte=datetime.date.today(),
                                                         discount__end_date__gte=datetime.date.today(),
                                                         discount__is_activate=True)

            for cart in carts:
                beer = cls.find_beer_by_cart(cart, beers)
                if beer is not None:
                    price = cart.beer.price
                    total_discount = total_discount + price * cart.amount
                    beer_discount = cls.find_beer_discount_by_beer(beer, beer_discounts)
                    if beer_discount is not None:
                        price = cart.beer.price - cart.beer.price * beer_discount.discount_percent / 100
                    total_price = total_price + price * cart.amount
            total_discount = total_discount - total_price

        user = GeneralInfoAccountSerializer(user)
        res_carts = BeerDetailCartSerializer(carts, many=True)
        res_data = {'user': user.data,
                    'carts': list(res_carts.data),
                    'total_price': total_price,
                    'total_price_usd': CurrencyConvertor.convert_vnd_to_usd(total_price),
                    'total_discount': total_discount}

        return res_data

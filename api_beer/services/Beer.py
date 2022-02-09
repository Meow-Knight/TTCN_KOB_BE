import datetime
import random
from dateutil.rrule import rrule, MONTHLY, DAILY

from django.db import transaction, connection

from api_beer.constants import SaleDurationEnum, SaleType
from api_beer.models import BeerPhoto, Beer, Discount, BeerShipment
from api_beer.serializers import ItemBeerSerializer, DiscountWithItemBeerSerializer, TopBeerSerializer
from api_beer.services import BeerPhotoService
from api_order.constants import OrderStatus
from api_order.models import Order, OrderDetail


class BeerService:

    @classmethod
    @transaction.atomic
    def create_beer_with_photos(cls, beer_serializer, images):
        beer = beer_serializer.save()
        beer_photos = []
        links = BeerPhotoService.upload_images(images)
        for link in links:
            beer_photos.append(BeerPhoto(link=link, beer=beer))
        BeerPhoto.objects.bulk_create(beer_photos)

    @classmethod
    def get_random_beers(cls, amount):
        all_records = list(Beer.objects.values_list('id', flat=True))
        random_records = random.sample(all_records, min(len(all_records), amount))
        return Beer.objects.filter(id__in=random_records)

    @classmethod
    def get_homepage_data(cls, random_amount):
        random_query_set = BeerService.get_random_beers(random_amount)
        random_serializer = ItemBeerSerializer(random_query_set, many=True)
        discount_query_set = Discount.objects.all()
        discount_serializer = DiscountWithItemBeerSerializer(discount_query_set, many=True)

        return {'randoms': random_serializer.data, 'discounts': discount_serializer.data}

    @classmethod
    def get_top_beers(cls, amount, enum_duration, enum_type):
        date_query = cls.get_date_query(enum_duration)
        beers = Beer.objects.raw("""SELECT beer_id AS id, SUM({}) AS total_sum
                        FROM `order` o
                        JOIN order_detail od ON od.order_id = o.id
                        WHERE o.done_at IS NOT NULL AND {} 
                        GROUP BY beer_id
                        ORDER BY total_sum DESC
                        LIMIT %s;""".format(cls.get_sum_field(enum_type), date_query), [amount, ])
        serializer = TopBeerSerializer(beers, many=True)
        data = serializer.data
        return data

    @classmethod
    def get_start_date(cls, enum_duration):
        switcher = {
            SaleDurationEnum.DAY: lambda: datetime.datetime.now() - datetime.timedelta(hours=24),
            SaleDurationEnum.WEEK: lambda: datetime.datetime.now() - datetime.timedelta(days=7),
            SaleDurationEnum.MONTH: lambda: datetime.datetime.now() - datetime.timedelta(days=30),
            SaleDurationEnum.YEAR: lambda: datetime.datetime.now() - datetime.timedelta(days=365)
        }
        return switcher.get(enum_duration)

    @classmethod
    def get_string_duration(cls, enum_duration):
        date_point = cls.get_start_date(enum_duration)
        if not date_point:
            return None
        date_string = date_point().strftime("%Y-%m-%d")
        return date_string

    @classmethod
    def get_date_query(cls, enum_duration):
        date_string = cls.get_string_duration(enum_duration)
        if not date_string:
            return " 1 = 1 "
        else:
            return " DATE(o.done_at) > '{}' ".format(date_string)

    @classmethod
    def get_sum_field(cls, enum_type):
        switcher = {
            SaleType.AMOUNT: "amount",
            SaleType.SALE: "o.total_price - o.total_discount"
        }
        return switcher.get(enum_type)

    @classmethod
    def get_chart_data(cls, enum_duration, enum_type):
        date_query = cls.get_date_query(enum_duration)
        cursor = connection.cursor()
        cursor.execute("""SELECT DATE(o.done_at) AS done_at, SUM({}) AS total
                        FROM `order` o
                        JOIN order_detail od ON od.order_id = o.id
                        WHERE o.done_at IS NOT NULL AND {}
                        GROUP BY DATE(o.done_at)
                        ORDER BY done_at DESC;""".format(cls.get_sum_field(enum_type), date_query, ))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    @classmethod
    def format_chart_data(cls, chart_data, enum_duration):
        start_date = cls.get_start_date(enum_duration)
        if not start_date:
            return None
        start_date = start_date()

        if enum_duration == SaleDurationEnum.YEAR:
            month_arr = {}
            for dt in rrule(MONTHLY, dtstart=start_date, until=datetime.datetime.now()):
                month_arr[dt.strftime("%Y-%m")] = 0
            for chart_record in chart_data:
                done_at = chart_record.get('done_at').strftime("%Y-%m")
                month_arr[done_at] += chart_record.get('total')
            return month_arr

        date_arr = {}
        for dt in rrule(DAILY, dtstart=start_date, until=datetime.datetime.now()):
            date_arr[dt.strftime("%Y-%m-%d")] = 0
        for chart_record in chart_data:
            done_at = chart_record.get('done_at').strftime("%Y-%m-%d")
            date_arr[done_at] = chart_record.get('total')
        return date_arr

    @classmethod
    @transaction.atomic
    def get_ids(cls, items):
        ids = []
        for item in items:
            ids.append(item.id)
        return ids

    @classmethod
    @transaction.atomic
    def get_data_for_sales_statistics(cls):
        completed_status = OrderStatus.COMPLETED.value.get("id")
        orders = Order.objects.filter(order_status=completed_status)
        order_ids = cls.get_ids(orders)
        order_details = OrderDetail.objects.filter(order__in=order_ids)
        order_detail_ids = cls.get_ids(order_details)
        beers = Beer.objects.filter(order_detail__in=order_detail_ids).distinct()
        beer_ids = cls.get_ids(beers)
        beer_shipments = BeerShipment.objects.filter(beer__in=beer_ids)
        return [orders, order_details, beer_shipments]

    @classmethod
    @transaction.atomic
    def get_sales_statistics(cls, request):
        my_data = cls.get_data_for_sales_statistics()
        orders = my_data[0]
        order_details = my_data[1]
        beer_shipments = my_data[2]
        total_revenue = 0.0
        total_sales = 0.0
        total_profit = 0.0
        total_root = 0.0
        if orders.exists():
            for order in orders:
                total_revenue = total_revenue + order.total_price

        if order_details.exists():
            for order_detail in order_details:
                total_sales = total_sales + order_detail.amount

        if beer_shipments.exists():
            for beer_shipment in beer_shipments:
                total_root = total_root + beer_shipment.price * beer_shipment.amount

        total_profit = total_revenue - total_root

        res_data = {"total_revenue": total_revenue, "total_sales": total_sales, "total_profit": total_profit}
        return res_data

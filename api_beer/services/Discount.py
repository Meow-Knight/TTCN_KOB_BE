from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from api_beer.models import BeerDiscount, Discount, Beer
from api_beer.serializers import DiscountSerializer, BeerDiscountSerializer, DropdownBeerSerializer


class DiscountService:

    @classmethod
    @transaction.atomic
    def create(cls, request_data):
        """
        return is_error, error_message, validated_data
        If is_error is True, error_message will have value as string and validated_data is None
        If is_error is False, error_message will be empty and validated_data is discount instance
        """

        discount_serializer = DiscountSerializer(data=request_data)
        if discount_serializer.is_valid(raise_exception=True):
            discount = discount_serializer.save()
            beers = request_data.get("beers")
            if not beers:
                raise ValidationError("Not found beers in discount data")

            for beer in beers:
                beer['discount'] = discount.id.hex
            beer_discount_ser = BeerDiscountSerializer(data=beers, many=True)
            if beer_discount_ser.is_valid(raise_exception=True):
                is_unique_all = cls.check_unique_beer_discount(beers)
                if not is_unique_all:
                    raise ValidationError({"details": "Duplicated beer and discount"})
                beer_ids = [beer.get('beer') for beer in beers]
                discount_start_date = request_data.get('start_date')
                discount_end_date = request_data.get('end_date')

                beer_discounts_existed_query_set = BeerDiscount.objects.filter(
                    (Q(discount__start_date__lte=discount_start_date)
                     & Q(discount__end_date__gte=discount_start_date))
                    | (Q(discount__start_date__lte=discount_end_date)
                       & Q(discount__end_date__gte=discount_end_date))
                    | (Q(start_date__gte=discount_start_date)
                       & Q(start_date__lte=discount_end_date)),
                    beer_id__in=beer_ids
                )
                if beer_discounts_existed_query_set.exists():
                    raise ValidationError({"details": "Beers already in another discount in this time range"})

                beer_discount_ser.save()
                return discount_serializer.data

    @classmethod
    def check_unique_beer_discount(cls, beers):
        kkk = set([(beer.get('beer'), beer.get('discount')) for beer in beers])
        return len(kkk) == len(beers)

    @classmethod
    def get_available_beers(cls, start_date, end_date):
        xx = Discount.objects.filter((Q(start_date__lte=start_date)
                                 & Q(end_date__gte=start_date))
                                | (Q(start_date__lte=end_date)
                                   & Q(end_date__gte=end_date))
                                | (Q(start_date__gte=start_date)
                                   & Q(start_date__lte=end_date))).values("beer_discount__beer")
        available_beer_qs = Beer.objects.exclude(id__in=Discount.objects.filter((Q(start_date__lte=start_date)
                                 & Q(end_date__gte=start_date))
                                | (Q(start_date__lte=end_date)
                                   & Q(end_date__gte=end_date))
                                | (Q(start_date__gte=start_date)
                                   & Q(start_date__lte=end_date))).values("beer_discount__beer")).values('id', 'name')

        return available_beer_qs

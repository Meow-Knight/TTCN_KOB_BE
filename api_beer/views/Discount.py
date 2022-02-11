from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.permissions import AdminPermission
from api_base.views import BaseViewSet
from api_beer.models import Discount
from api_beer.serializers import DiscountSerializer, DetailDiscountSerializer
from api_beer.services import DiscountService


class DiscountViewSet(BaseViewSet):
    permission_classes = [AdminPermission]
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    serializer_map = {
        "retrieve": DetailDiscountSerializer
    }
    permission_map =  {
        "get_available_beers": []
    }

    def create(self, request, *args, **kwargs):
        validated_data = DiscountService.create(request.data)
        return Response(validated_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def get_available_beers(self, request, *args, **kwargs):
        start_date_str = request.query_params.get("start_date", "")
        end_date_str = request.query_params.get("end_date", "")

        if not start_date_str or not end_date_str:
            return Response({"detail": "Not found start_date and end_date in url param"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            if start_date > end_date:
                raise ValueError
        except ValueError:
            return Response({"detail": "Invalid start_date/end_date"}, status=status.HTTP_400_BAD_REQUEST)

        available_beers = DiscountService.get_available_beers(start_date, end_date)
        return Response(available_beers)

from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api_beer.serializers import ProducerSerializer, DropdownProducerSerializer
from api_beer.models import Producer
from api_base.views import BaseViewSet


class CreateProducerViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()
    permission_map = {
        "list": [],
        "retrieve": [],
        "get_all_with_name": []
    }

    def list(self, request, *args, **kwargs):
        query_set = Producer.objects
        search_query = request.query_params.get("q", "")
        query_set = query_set.filter(name__icontains=search_query)
        sort_query = request.query_params.get("sort")
        if sort_query:
            try:
                if sort_query.startswith("-"):
                    Producer._meta.get_field(sort_query[1:])
                else:
                    Producer._meta.get_field(sort_query)
                query_set = query_set.order_by(sort_query)
            except:
                pass

        self.queryset = query_set
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def get_all_with_name(self, request, *args, **kwargs):
        return Response(DropdownProducerSerializer(self.get_queryset(), many=True).data)

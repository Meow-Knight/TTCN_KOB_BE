from rest_framework import viewsets

from api_beer.serializers import ProducerSerializer
from api_beer.models import Producer


class CreateProducerViewSet(viewsets.ModelViewSet):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()

from rest_framework import viewsets

from api_admin.serializers import ProducerSerializer
from api_admin.models import Producer


class CreateProducerViewSet(viewsets.ModelViewSet):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()

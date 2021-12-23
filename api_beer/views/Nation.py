from rest_framework import viewsets

from api_beer.serializers import NationSerializer
from api_beer.models import Nation


class NationViewSet(viewsets.ModelViewSet):
    serializer_class = NationSerializer
    queryset = Nation.objects.all()

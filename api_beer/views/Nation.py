from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api_beer.serializers import NationSerializer
from api_beer.models import Nation


class NationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = NationSerializer
    queryset = Nation.objects.all()

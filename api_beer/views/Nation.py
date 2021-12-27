from rest_framework.permissions import IsAdminUser

from api_beer.serializers import NationSerializer
from api_beer.models import Nation
from api_base.views import BaseViewSet


class NationViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = NationSerializer
    queryset = Nation.objects.all()
    permission_map = {
        "list": [],
        "retrieve": []
    }

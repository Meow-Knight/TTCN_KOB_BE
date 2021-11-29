from rest_framework import viewsets

from api_account.serializers import RoleSerializer
from api_account.models import Role


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

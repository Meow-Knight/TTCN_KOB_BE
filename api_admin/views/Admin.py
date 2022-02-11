from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.constants import RoleData
from api_account.permissions import AdminPermission
from api_admin.serializers import CreateAccountSerializer
from api_base.views import BaseViewSet


class AdminViewSet(BaseViewSet):
    permission_classes = [AdminPermission]

    @action(detail=False, methods=['post'])
    def create_staff(self, request, *args, **kwargs):
        request.data['role'] = RoleData.STAFF.value.get('id')
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

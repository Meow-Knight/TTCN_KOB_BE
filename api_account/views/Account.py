from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_account.models import Account
from api_account.permissions import StaffOrAdminPermission, AdminPermission
from api_account.serializers import AccountInfoSerializer, GeneralInfoAccountSerializer, LoginAccountSerializer, \
    ListAccountSerializer
from api_account.services import AccountService
from api_account.constants import RoleData
from api_base.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountInfoSerializer
    queryset = Account.objects.all()
    serializer_map = {
        "detail": GeneralInfoAccountSerializer,
        "change_password": LoginAccountSerializer,
        "list": ListAccountSerializer,
        "customers": ListAccountSerializer,
        "staffs": ListAccountSerializer
    }
    permission_map = {
        "change_password": [StaffOrAdminPermission],
        "customers": [AdminPermission],
        "partial_update": [],
        "staffs": [AdminPermission]
    }

    @action(detail=False, methods=['get'])
    def info(self, request, *args, **kwargs):
        user = self.request.user
        serializer = AccountInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def edit(self, request, *args, **kwargs):
        account = request.user
        avatar = request.FILES.get('avatar')
        if avatar:
            avatar_link = AccountService.upload_avatar(avatar)
            request.data['avatar'] = avatar_link
        serializer = GeneralInfoAccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def change_password(self, request, *args, **kwargs):
        account = request.user
        serializer = self.get_serializer(account, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def customers(self, request, *args, **kwargs):
        self.queryset = Account.objects.filter(role_id=RoleData.CUSTOMER.value.get('id'))
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def staffs(self, request, *args, **kwargs):
        self.queryset = Account.objects.filter(role_id=RoleData.STAFF.value.get('id'))
        return super().list(request, *args, **kwargs)

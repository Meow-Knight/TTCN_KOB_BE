from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_account.models import Account
from api_account.serializers import AccountInfoSerializer, GeneralInfoAccountSerializer
from api_base.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountInfoSerializer # tmp serializer
    queryset = Account.objects.all()
    serializer_map = {
        "detail": GeneralInfoAccountSerializer
    }

    @action(detail=False, methods=['get'])
    def info(self, request, *args, **kwargs):
        user = self.request.user
        serializer = AccountInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def edit(self, request, *args, **kwargs):
        account = request.user
        serializer = GeneralInfoAccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.serializers import AccountInfoSerializer
from api_account.models import Account


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountInfoSerializer # tmp serializer
    queryset = Account.objects.all()

    @action(detail=False, methods=['get'])
    def info(self, request, *args, **kwargs):
        user = self.request.user
        serializer = AccountInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

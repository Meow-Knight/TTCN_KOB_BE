from rest_framework import serializers

from api_account.models import Account
from api_base.serializers import ReadOnlyModelSerializer


class AccountInfoSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_superuser', 'phone', 'age', 'address')


class GeneralInfoAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'role', 'is_active', 'is_staff', 'is_superuser')


class SimpleAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'avatar')

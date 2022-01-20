from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api_account.models import Account
from api_base.serializers import ReadOnlyModelSerializer


class AccountInfoSerializer(ReadOnlyModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_superuser', 'phone', 'age', 'address', 'avatar', 'role')


class GeneralInfoAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'role', 'is_active', 'is_staff', 'is_superuser')


class SimpleAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'avatar')


class AccountInforOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'age', 'first_name', 'last_name')


class LoginAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'password')

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        for attr, value in validated_data.items():
            if attr == 'password':
                value = make_password(value)
            setattr(instance, attr, value)
        instance.save()

        return instance

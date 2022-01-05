from rest_framework import serializers

from api_account.models import Account


class AccountInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff')


class AccountInforCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email','address', 'phone', 'age')

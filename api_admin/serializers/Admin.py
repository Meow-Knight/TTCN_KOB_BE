from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api_account.models import Account


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'password', 'email', 'address', 'phone', 'age', 'role')

    def validate(self, attrs):
        password = attrs.get('password')
        attrs['password'] = make_password(password)
        return attrs

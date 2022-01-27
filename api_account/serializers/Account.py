from django.contrib.auth.hashers import make_password
from django.db.models import Sum, F
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api_account.models import Account
from api_order.constants import OrderStatus


class AccountInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_staff', 'is_superuser', 'phone', 'age', 'address', 'avatar', 'role', 'is_active')


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


class ListAccountSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()
    total_sale = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'full_name', 'username', 'date_joined', 'order_count', 'total_sale', 'is_active')

    def get_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    def get_order_count(self, obj):
        return len(obj.order.all())

    def get_total_sale(self, obj):
        data = obj.order.filter(order_status_id=OrderStatus.COMPLETED.value.get('id')).aggregate(sale=(Sum('total_price') - Sum('total_discount')))
        return data['sale']

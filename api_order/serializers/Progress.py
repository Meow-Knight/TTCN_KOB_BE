from rest_framework import serializers

from api_order.models import Progress
from api_order.serializers import RetrieveOrderStatus


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'


class RetrieveProgressSerializer(serializers.ModelSerializer):
    order_status = RetrieveOrderStatus()

    def to_representation(self, instance):
        data = super(RetrieveProgressSerializer, self).to_representation(instance)
        data['order_status'] = data['order_status'].get('name')
        return data

    class Meta:
        model = Progress
        fields = ['id', 'order_status', 'created_at', 'updated_at', ]

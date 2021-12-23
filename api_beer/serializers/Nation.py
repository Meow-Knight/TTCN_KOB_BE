from rest_framework import serializers

from api_beer.models import Nation


class NationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = '__all__'

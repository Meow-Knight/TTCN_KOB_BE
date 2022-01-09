from rest_framework import serializers

from api_account.models import Review
from api_account.serializers import SimpleAccountSerializer


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class ListReviewByBeerSerializer(serializers.ModelSerializer):
    account = SimpleAccountSerializer()

    class Meta:
        model = Review
        exclude = ('beer',)
        depth = 1

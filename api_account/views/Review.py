from django.db.models import Case, When, Avg
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.serializers import ReviewSerializer, ListReviewByBeerSerializer
from api_account.services import ReviewService
from api_account.models import Review
from api_base.views import BaseViewSet
from api_beer.models import Beer


class ReviewViewSet(BaseViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    serializer_map = {
        "get_by_beer": ListReviewByBeerSerializer
    }
    permission_map = {
        "get_by_beer": [],
        "list": [],
        "rate": []
    }

    def create(self, request, *args, **kwargs):
        request.data['account'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            beer = serializer.validated_data.get('beer')
            if ReviewService.can_create_review(request.user, beer):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "You cannot create review on this beer. You have to buy it before"},
                                status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.account == request.user:
            request.data['account'] = request.user.id
            return super().update(request, **kwargs)
        return Response({"details": "You are not the owner of this review"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.account == request.user:
            kwargs['partial'] = True
            return super(ReviewViewSet, self).update(request, **kwargs)
        else:
            return Response({"details": "You are not the owner of this review"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_by_beer(self, request, *args, **kwargs):
        beer_id = request.query_params.get("beer_id")
        try:
            rate = int(request.query_params.get("rate"))
        except ValueError:
            rate = 0
        if not beer_id:
            return Response({"detail": "Beer id param not found"}, status=status.HTTP_400_BAD_REQUEST)
        beer = Beer.objects.filter(id=beer_id)
        if not beer.exists():
            return Response({"detail": "Beer id is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        if not (1 <= rate <= 5):
            return Response({"detail": "Rate is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        beer = beer.first()
        if rate:
            review_qs = Review.objects.filter(beer=beer, rate=rate)
        else:
            review_qs = Review.objects.filter(beer=beer)
        if not request.user.is_anonymous:
            account = request.user
            review_qs = review_qs.order_by(Case(When(account=account, then=0), default=1),
                                           '-updated_at')
        else:
            review_qs.order_by('-updated_at')
        self.queryset = review_qs
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        account = request.user
        if review.account == account:
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You are not the owner of this review"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_can_review(self, request, *args, **kwargs):
        beer_id = request.query_params.get("beer_id")
        beer = Beer.objects.filter(id=beer_id)
        if not beer.exists():
            return Response({"detail": "Invalid beer id in url param"}, status=status.HTTP_400_BAD_REQUEST)
        account = request.user
        beer = beer.first()
        if ReviewService.can_create_review(account, beer):
            return Response({"detail": True})
        else:
            return Response({"detail": False})

    @action(detail=False, methods=['get'])
    def rate(self, request, *args, **kwargs):
        beer_id = request.query_params.get("beer_id")
        beer = Beer.objects.filter(id=beer_id)
        if not beer:
            return Response({"detail": "Invalid beer id in url param"}, status=status.HTTP_400_BAD_REQUEST)
        beer = beer.first()
        rate = Review.objects.filter(beer=beer).aggregate(beer_avg_rate=Avg('rate'))
        return Response(rate, status=status.HTTP_200_OK)

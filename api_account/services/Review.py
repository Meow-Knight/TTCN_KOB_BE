from api_account.models import Review
from api_order.models import OrderDetail, OrderStatus
from api_order import constants


class ReviewService:
    @classmethod
    def can_create_review(cls, account, beer):
        done_status = OrderStatus.objects.get(id=constants.OrderStatus.COMPLETED.value.get('id'))
        if OrderDetail.objects.filter(beer=beer, order__account=account, order__order_status=done_status).exists():
            return not Review.objects.filter(account=account, beer=beer).exists()
        return False

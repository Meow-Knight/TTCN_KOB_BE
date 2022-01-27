from django.db import  models

from api_base.models import TimeStampedModel
from api_order.models import Order, PaymentMethod


class Payment(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name="payment")
    id_paypal = models.CharField(max_length=100, null=True)
    email_paypal = models.EmailField(unique=False, null=True)

    class Meta:
        db_table = "payment"
        ordering = ('-created_at',)

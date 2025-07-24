# =======================================================================
# FILE: myduka/payments/models.py (EDITED)
# =======================================================================
from django.db import models
from stores.models import StockReceive

class MpesaTransaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    stock_receive = models.OneToOneField(StockReceive, on_delete=models.CASCADE, related_name='mpesa_transaction')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mpesa Payment for Stock ID: {self.stock_receive.id}"

# =======================================================================
# FILE: myduka/stores/models.py
# =======================================================================
from django.db import models
from django.conf import settings

class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventory')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f"{self.name} ({self.store.name})"

class StockReceive(models.Model):
    class PaymentStatus(models.TextChoices):
        PAID = "paid", "Paid"
        UNPAID = "unpaid", "Unpaid"

    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='received_stock')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='deliveries')
    quantity_received = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    received_at = models.DateTimeField(auto_now_add=True)

class Spoilage(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='spoilages')
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    logged_at = models.DateTimeField(auto_now_add=True)

class SupplyRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        DECLINED = "declined", "Declined"
        RECEIVED = "received", "Received"

    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='supply_requests')
    quantity_requested = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    supplier_phone_number = models.CharField(max_length=20, blank=True, null=True)

class Sale(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        MPESA = "mpesa", "M-Pesa"

    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='sales')
    quantity_sold = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    sold_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sold_at = models.DateTimeField(auto_now_add=True)

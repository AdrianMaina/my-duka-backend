# =======================================================================
# FILE: myduka/stores/models.py (EDITED)
# =======================================================================
from django.db import models
from django.conf import settings

class Store(models.Model):
    # Using settings.AUTH_USER_MODEL is best practice and works here
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventory')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f"{self.name} ({self.store.name})"

# Add other models like Supplier, SpoilageLog etc. here

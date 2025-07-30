# =======================================================================
# FILE: myduka/stores/admin.py (FIXED)
# =======================================================================
from django.contrib import admin
from .models import Store, InventoryItem, Supplier, StockReceive, Spoilage, SupplyRequest, Sale

admin.site.register(Store)
admin.site.register(InventoryItem)
admin.site.register(Supplier)
admin.site.register(StockReceive)
admin.site.register(Spoilage)
admin.site.register(SupplyRequest)
admin.site.register(Sale)

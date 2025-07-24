# =======================================================================
# FILE: myduka/stores/urls.py
# =======================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, InventoryItemViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'inventory', InventoryItemViewSet, basename='inventoryitem')

urlpatterns = [
    path('', include(router.urls)),
]
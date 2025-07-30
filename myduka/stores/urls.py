# =======================================================================
# FILE: myduka/stores/urls.py (FIXED)
# =======================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StoreViewSet, InventoryItemViewSet, SupplierViewSet, 
    StockReceiveViewSet, SpoilageViewSet, SupplyRequestViewSet,
    MarkAsPaidView, SaleViewSet, ApprovedSupplyRequestsView, ConfirmDeliveryView
)

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'inventory', InventoryItemViewSet, basename='inventoryitem')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'stock-receive', StockReceiveViewSet, basename='stockreceive')
router.register(r'spoilage', SpoilageViewSet, basename='spoilage')
router.register(r'supply-requests', SupplyRequestViewSet, basename='supplyrequest') # This line creates the URL
router.register(r'sales', SaleViewSet, basename='sale')

urlpatterns = [
    path('', include(router.urls)),
    path('stock-receive/<int:pk>/mark-as-paid/', MarkAsPaidView.as_view(), name='mark-as-paid'),
    path('approved-supply-requests/', ApprovedSupplyRequestsView.as_view(), name='approved-supply-requests'),
    path('supply-requests/<int:pk>/confirm-delivery/', ConfirmDeliveryView.as_view(), name='confirm-delivery'),
]
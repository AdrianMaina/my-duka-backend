# =======================================================================
# FILE: myduka/payments/urls.py (EDITED)
# =======================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MpesaTransactionViewSet, UnpaidDeliveriesListView, PaySupplierView, MpesaCallbackView

router = DefaultRouter()
router.register(r'transactions', MpesaTransactionViewSet, basename='mpesatransaction')

urlpatterns = [
    path('', include(router.urls)),
    path('unpaid-deliveries/', UnpaidDeliveriesListView.as_view(), name='unpaid-deliveries'),
    path('pay-supplier/', PaySupplierView.as_view(), name='pay-supplier'),
    path('mpesa-callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
]
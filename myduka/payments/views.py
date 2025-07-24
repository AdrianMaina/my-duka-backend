# =======================================================================
# FILE: myduka/payments/views.py (EDITED)
# =======================================================================
from rest_framework import viewsets, permissions, generics
from .models import MpesaTransaction
from .serializers import MpesaTransactionSerializer, UnpaidDeliverySerializer
from stores.models import StockReceive

class MpesaTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MpesaTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        store_id = self.request.query_params.get('store_id')

        if user.role == 'merchant' and store_id:
            return MpesaTransaction.objects.filter(
                stock_receive__inventory_item__store_id=store_id,
                stock_receive__inventory_item__store__owner=user
            )
        
        return MpesaTransaction.objects.none()

class UnpaidDeliveriesListView(generics.ListAPIView):
    serializer_class = UnpaidDeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        store_id = self.request.query_params.get('store_id')

        if user.role == 'merchant' and store_id:
            return StockReceive.objects.filter(
                inventory_item__store_id=store_id,
                inventory_item__store__owner=user,
                payment_status=StockReceive.PaymentStatus.UNPAID
            )
        return StockReceive.objects.none()

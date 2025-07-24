# =======================================================================
# FILE: myduka/stores/views.py
# =======================================================================
from rest_framework import viewsets, permissions
from .models import Store, InventoryItem
from .serializers import StoreSerializer, InventoryItemSerializer
from users.permissions import IsMerchant

class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, IsMerchant]

    def get_queryset(self):
        # Merchants can only see their own stores
        return Store.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in merchant as the owner
        serializer.save(owner=self.request.user)

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'merchant':
            # A merchant can see inventory for any of their stores
            return InventoryItem.objects.filter(store__owner=user)
        elif user.role == 'admin' or user.role == 'clerk':
            # Admins/Clerks can only see inventory for their assigned store
            return InventoryItem.objects.filter(store=user.store)
        return InventoryItem.objects.none()

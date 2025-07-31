# =======================================================================
# FILE: myduka/stores/views.py (FIXED)
# =======================================================================
from rest_framework import viewsets, permissions, status, serializers, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Store, InventoryItem, Supplier, StockReceive, Spoilage, SupplyRequest, Sale
from .serializers import StoreSerializer, InventoryItemSerializer, SupplierSerializer, StockReceiveSerializer, SpoilageSerializer, SupplyRequestSerializer, SaleSerializer, ApprovedSupplyRequestSerializer, ConfirmDeliverySerializer
from users.permissions import IsMerchant, IsAdmin, IsClerk
from reports.models import DailySale
from django.utils import timezone

class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, IsMerchant]
    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'merchant':
            return InventoryItem.objects.filter(store__owner=user)
        return InventoryItem.objects.filter(store=user.store)

class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'merchant':
            return Supplier.objects.filter(store__owner=user)
        return Supplier.objects.filter(store=user.store)

class StockReceiveViewSet(viewsets.ModelViewSet):
    serializer_class = StockReceiveSerializer
    permission_classes = [permissions.IsAuthenticated, IsClerk | IsAdmin]
    def get_queryset(self):
        return StockReceive.objects.filter(inventory_item__store=self.request.user.store)
    def perform_create(self, serializer):
        stock_receive = serializer.save()
        item = stock_receive.inventory_item
        item.quantity += stock_receive.quantity_received
        item.save()

class SpoilageViewSet(viewsets.ModelViewSet):
    serializer_class = SpoilageSerializer
    permission_classes = [permissions.IsAuthenticated, IsClerk | IsAdmin]
    def get_queryset(self):
        return Spoilage.objects.filter(inventory_item__store=self.request.user.store)
    def perform_create(self, serializer):
        spoilage = serializer.save()
        item = spoilage.inventory_item
        item.quantity -= spoilage.quantity
        item.save()

class SupplyRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SupplyRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return SupplyRequest.objects.filter(inventory_item__store=user.store)
        elif user.role == 'clerk':
            return SupplyRequest.objects.filter(requested_by=user)
        return SupplyRequest.objects.none()
    
    def get_serializer_context(self):
        # Ensures serializer has access to `request.user` inside validation
        return {'request': self.request}

class MarkAsPaidView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def patch(self, request, pk, *args, **kwargs):
        try:
            stock_receive = StockReceive.objects.get(pk=pk, inventory_item__store=request.user.store)
            stock_receive.payment_status = StockReceive.PaymentStatus.PAID
            stock_receive.save()
            serializer = StockReceiveSerializer(stock_receive)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StockReceive.DoesNotExist:
            return Response({"error": "Stock receive record not found."}, status=status.HTTP_404_NOT_FOUND)

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsClerk]

    def get_queryset(self):
        return Sale.objects.filter(sold_by=self.request.user)

    def perform_create(self, serializer):
        item = serializer.validated_data['inventory_item']
        quantity_sold = serializer.validated_data['quantity_sold']

        if item.quantity < quantity_sold:
            raise serializers.ValidationError("Not enough stock to complete the sale.")

        # 1. Deduct from inventory
        item.quantity -= quantity_sold
        item.save()

        # 2. Save the individual sale record
        sale = serializer.save(sold_by=self.request.user)

        # 3. Update the daily sales summary for reporting
        sale_date = sale.sold_at.date()
        sale_value = quantity_sold * item.selling_price

        daily_sale, created = DailySale.objects.get_or_create(
            store=item.store,
            date=sale_date,
            defaults={'total_sales': 0}
        )
        daily_sale.total_sales += sale_value
        daily_sale.save()


class ApprovedSupplyRequestsView(generics.ListAPIView):
    serializer_class = ApprovedSupplyRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsClerk]

    def get_queryset(self):
        return SupplyRequest.objects.filter(
            inventory_item__store=self.request.user.store,
            status=SupplyRequest.Status.APPROVED
        )

class ConfirmDeliveryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClerk]

    def post(self, request, pk, *args, **kwargs):
        serializer = ConfirmDeliverySerializer(data=request.data)
        if serializer.is_valid():
            try:
                supply_request = SupplyRequest.objects.get(
                    pk=pk, 
                    inventory_item__store=request.user.store,
                    status=SupplyRequest.Status.APPROVED
                )
                
                phone_number = serializer.validated_data['supplier_phone_number']
                
                supplier, created = Supplier.objects.get_or_create(
                    store=supply_request.inventory_item.store,
                    phone_number=phone_number,
                    defaults={'name': f"Supplier {phone_number}"}
                )

                StockReceive.objects.create(
                    inventory_item=supply_request.inventory_item,
                    supplier=supplier,
                    quantity_received=supply_request.quantity_requested,
                    payment_status=StockReceive.PaymentStatus.UNPAID
                )

                item = supply_request.inventory_item
                item.quantity += supply_request.quantity_requested
                item.save()

                supply_request.status = SupplyRequest.Status.RECEIVED
                supply_request.supplier_phone_number = phone_number
                supply_request.save()

                return Response({'status': 'Delivery confirmed'}, status=status.HTTP_200_OK)

            except SupplyRequest.DoesNotExist:
                return Response({"error": "Approved supply request not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =======================================================================
# FILE: myduka/reports/views.py (FIXED)
# =======================================================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Sum, Count, F
from stores.models import Store, InventoryItem, StockReceive, Spoilage, SupplyRequest
from users.models import User
from .models import DailySale
from .serializers import StaffSerializer
import traceback

class StoreOverviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, store_id, *args, **kwargs):
        try:
            store = Store.objects.get(pk=store_id, owner=request.user)
        except Store.DoesNotExist:
            return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

        total_staff = store.staff.count()
        monthly_sales = DailySale.objects.filter(
            store=store,
            date__month=timezone.now().month
        ).aggregate(total=Sum('total_sales'))['total'] or 0
        
        pending_payments = StockReceive.objects.filter(
            inventory_item__store=store,
            payment_status=StockReceive.PaymentStatus.UNPAID
        ).count()

        data = {
            "totalStaff": total_staff,
            "monthlySales": float(monthly_sales),
            "pendingPayments": pending_payments
        }
        return Response(data, status=status.HTTP_200_OK)


def get_queryset(self):
    store_id = self.kwargs.get('store_id')
    requesting_user = self.request.user

    try:
        print(f"Getting store with ID: {store_id}, for user {requesting_user.username}")
        store = Store.objects.get(pk=store_id, owner=requesting_user)

        staff_queryset = store.staff.exclude(pk=requesting_user.pk)

        print(f"Staff members: {[s.username for s in staff_queryset]}")
        return staff_queryset

    except Exception as e:
        print("!!! ERROR in StaffListAPIView !!!")
        print(traceback.format_exc())  # Full traceback
        return User.objects.none()


class SalesChartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, store_id, *args, **kwargs):
        try:
            store = Store.objects.get(pk=store_id, owner=request.user)
        except Store.DoesNotExist:
            return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)
        
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=6)
        
        sales = DailySale.objects.filter(
            store=store,
            date__range=[seven_days_ago, today]
        ).order_by('date')

        sales_dict = {sale.date.strftime('%a'): sale.total_sales for sale in sales}
        
        chart_data = []
        for i in range(7):
            day = seven_days_ago + timedelta(days=i)
            day_abbr = day.strftime('%a')
            chart_data.append({
                "name": day_abbr,
                "Sales": float(sales_dict.get(day_abbr, 0))
            })
            
        return Response(chart_data, status=status.HTTP_200_OK)

class AdminOverviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        admin_user = request.user
        if not admin_user.store:
            return Response({"error": "Admin not assigned to a store"}, status=status.HTTP_400_BAD_REQUEST)

        store = admin_user.store

        spoilage_patterns = Spoilage.objects.filter(inventory_item__store=store)\
            .values('reason').annotate(count=Count('id'))
        
        stock_trends_data = []

        data = {
            "spoilageData": list(spoilage_patterns),
            "stockTrendsData": stock_trends_data
        }
        return Response(data, status=status.HTTP_200_OK)

class ClerkOverviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        clerk_user = request.user
        if not clerk_user.store:
            return Response({"error": "Clerk not assigned to a store"}, status=status.HTTP_400_BAD_REQUEST)

        store = clerk_user.store
        today = date.today()
        one_week_ago = today - timedelta(days=7)

        items_received_today = StockReceive.objects.filter(
            inventory_item__store=store, received_at__date=today
        ).aggregate(total=Sum('quantity_received'))['total'] or 0

        low_stock_items = InventoryItem.objects.filter(
            store=store, quantity__lt=F('reorder_level')
        ).count()

        spoilage_incidents_week = Spoilage.objects.filter(
            inventory_item__store=store, logged_at__date__gte=one_week_ago
        ).count()

        pending_requests = SupplyRequest.objects.filter(
            inventory_item__store=store, status=SupplyRequest.Status.PENDING
        ).count()

        data = {
            "itemsReceived": items_received_today,
            "lowStockItems": low_stock_items,
            "spoilageCount": spoilage_incidents_week,
            "pendingRequests": pending_requests,
        }
        return Response(data, status=status.HTTP_200_OK)


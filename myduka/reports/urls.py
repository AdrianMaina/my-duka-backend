=======================================================================
FILE: myduka/reports/urls.py (FIXED)
=======================================================================
from django.urls import path
from .views import (
    StoreOverviewAPIView, StaffListAPIView, SalesChartAPIView, 
    AdminOverviewAPIView, ClerkOverviewAPIView
)

urlpatterns = [
    path('overview/<int:store_id>/', StoreOverviewAPIView.as_view(), name='store-overview'),
    path('staff-list/<int:store_id>/', StaffListAPIView.as_view(), name='staff-list'),
    path('sales-chart/<int:store_id>/', SalesChartAPIView.as_view(), name='sales-chart'),
    path('admin-overview/', AdminOverviewAPIView.as_view(), name='admin-overview'),
    path('clerk-overview/', ClerkOverviewAPIView.as_view(), name='clerk-overview'),
]
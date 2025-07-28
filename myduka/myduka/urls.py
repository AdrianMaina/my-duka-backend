# =======================================================================
# FILE: myduka/myduka/urls.py
# =======================================================================
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/', include('stores.urls')),
]

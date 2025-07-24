# =======================================================================
# FILE: myduka/payments/admin.py (NEW)
# =======================================================================
from django.contrib import admin
from .models import MpesaTransaction

admin.site.register(MpesaTransaction)


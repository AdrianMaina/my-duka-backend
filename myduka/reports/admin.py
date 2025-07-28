=======================================================================
FILE: myduka/reports/admin.py (NEW)
=======================================================================
from django.contrib import admin
from .models import DailySale

admin.site.register(DailySale)

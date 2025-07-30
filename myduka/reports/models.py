#=======================================================================
#FILE: myduka/reports/models.py (NEW)
#=======================================================================
from django.db import models
from stores.models import Store

class DailySale(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='sales')
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)

class Meta:
    unique_together = ('store', 'date')

def __str__(self):
    return f"Sales for {self.store.name} on {self.date}"
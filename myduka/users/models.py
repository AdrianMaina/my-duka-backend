# =======================================================================
# FILE: myduka/users/models.py
# =======================================================================
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        MERCHANT = "merchant", "Merchant"
        ADMIN = "admin", "Admin"
        CLERK = "clerk", "Clerk"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.MERCHANT)
    
    # A user can be associated with one store (for Admins and Clerks)
    # Merchants are not tied to a single store, they own them.
    store = models.ForeignKey(
        'stores.Store', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='staff'
    )
# =======================================================================
# FILE: myduka/users/permissions.py
# =======================================================================
from rest_framework.permissions import BasePermission
from .models import User

class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.MERCHANT

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.ADMIN

class IsClerk(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.CLERK

=======================================================================
FILE: myduka/reports/serializers.py (NEW)
=======================================================================
from rest_framework import serializers
from users.models import User

class StaffSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

class Meta:
    model = User
    fields = ['id', 'name', 'email', 'role', 'status']

def get_name(self, obj):
    return obj.get_full_name() or obj.username

def get_status(self, obj):
    # This logic can be expanded later to check invite expiry
    return "verified" if obj.is_active else "pending"
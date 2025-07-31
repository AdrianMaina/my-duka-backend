#=======================================================================
#FILE: myduka/reports/serializers.py (NEW)
#=======================================================================
from rest_framework import serializers
from users.models import User

class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for listing staff members, including their role, status,
    and the name of the store they are assigned to.
    """
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField() # Changed to a method field for safety

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'status', 'is_active', 'store_name']

    def get_name(self, obj):
        """Returns the user's full name, or their username as a fallback."""
        return obj.get_full_name() or obj.username

    def get_status(self, obj):
        """Determines the user's status based on whether their account is active."""
        return "verified" if obj.is_active else "pending"

    def get_store_name(self, obj):
        return getattr(obj.store, 'name', None)

        

class Meta:
    model = User
    fields = ['id', 'name', 'email', 'role', 'status']

def get_name(self, obj):
    return obj.get_full_name() or obj.username

def get_status(self, obj):
    # This logic can be expanded later to check invite expiry
    return "verified" if obj.is_active else "pending"

class StaffSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    store_name = serializers.CharField(source='store.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'status', 'is_active']

    def get_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_status(self, obj):
        # This logic can be expanded later to check invite expiry
        return "verified" if obj.is_active else "pending"

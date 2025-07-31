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
        """Safely returns the name of the user's store, or None if they have no store."""
        # This check prevents crashes if a user somehow has no store assigned.
        if hasattr(obj, 'store') and obj.store is not None:
            return obj.store.name
        return None



# FILE: myduka/stores/serializers.py
# =======================================================================
from rest_framework import serializers
from .models import Store, InventoryItem

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'owner']
        read_only_fields = ['owner']

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'store', 'name', 'quantity', 'reorder_level']
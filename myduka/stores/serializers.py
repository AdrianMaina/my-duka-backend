# =======================================================================
# FILE: myduka/stores/serializers.py (FIXED)
# =======================================================================
from rest_framework import serializers
from .models import Store, InventoryItem, Supplier, StockReceive, Spoilage, SupplyRequest, Sale

class StoreSerializer(serializers.ModelSerializer):
    staff_count = serializers.IntegerField(source='staff.count', read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'owner', 'staff_count']
        read_only_fields = ['owner']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class StockReceiveSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='inventory_item.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = StockReceive
        fields = ['id', 'product_name', 'supplier_name', 'quantity_received', 'payment_status', 'received_at']

class SpoilageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spoilage
        fields = '__all__'

class SupplyRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(write_only=True, required=False) # Optional for updates
    inventory_item_name = serializers.CharField(source='inventory_item.name', read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.username', read_only=True)

    class Meta:
        model = SupplyRequest
        fields = [
            'id', 'inventory_item', 'inventory_item_name', 'product_name',
            'quantity_requested', 'status', 'requested_by', 'requested_by_name', 'requested_at'
        ]
        read_only_fields = ['requested_by', 'inventory_item']

    def validate(self, data):
        # For create operations ('POST'), 'product_name' is required.
        if not self.instance and 'product_name' not in data:
            raise serializers.ValidationError({"product_name": "This field is required."})
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        product_name = validated_data.pop('product_name')
        try:
            inventory_item = InventoryItem.objects.get(name__iexact=product_name, store=user.store)
        except InventoryItem.DoesNotExist:
            raise serializers.ValidationError(f"Product '{product_name}' not found in your store's inventory.")
        
        validated_data['inventory_item'] = inventory_item
        validated_data['requested_by'] = user
        return super().create(validated_data)

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ['sold_by']

class ApprovedSupplyRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='inventory_item.name', read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.username', read_only=True)

    class Meta:
        model = SupplyRequest
        fields = ['id', 'product_name', 'quantity_requested', 'requested_by_name', 'requested_at']

class ConfirmDeliverySerializer(serializers.Serializer):
    supplier_phone_number = serializers.CharField(max_length=20)

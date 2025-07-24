# =======================================================================
# FILE: myduka/payments/serializers.py (EDITED)
# =======================================================================
from rest_framework import serializers
from .models import MpesaTransaction
from stores.models import StockReceive

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = '__all__'

class UnpaidDeliverySerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    supplier_phone = serializers.CharField(source='supplier.phone_number', read_only=True)
    product_name = serializers.CharField(source='inventory_item.name', read_only=True)
    amount = serializers.SerializerMethodField()

    class Meta:
        model = StockReceive
        fields = ['id', 'supplier_name', 'supplier_phone', 'product_name', 'quantity_received', 'amount']

    def get_amount(self, obj):
        return obj.quantity_received * obj.inventory_item.buying_price
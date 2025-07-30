# =======================================================================
# FILE: myduka/payments/views.py (FIXED)
# =======================================================================
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView # ADDED THIS IMPORT
from .models import MpesaTransaction
from .serializers import MpesaTransactionSerializer, UnpaidDeliverySerializer
from stores.models import StockReceive
from .utils import lipa_na_mpesa_online
import re

def format_phone_number(phone):
    """Formats phone number to 254... format."""
    if not phone:
        return None
    phone = "".join(filter(str.isdigit, phone))
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    elif phone.startswith('+254'):
        phone = phone[1:]
    
    if len(phone) == 12 and phone.startswith('254'):
        return phone
    return None

class MpesaTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MpesaTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        store_id = self.request.query_params.get('store_id')

        if user.role == 'merchant' and store_id:
            return MpesaTransaction.objects.filter(
                stock_receive__inventory_item__store_id=store_id,
                stock_receive__inventory_item__store__owner=user
            )
        
        return MpesaTransaction.objects.none()

class UnpaidDeliveriesListView(generics.ListAPIView):
    serializer_class = UnpaidDeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        store_id = self.request.query_params.get('store_id')

        if user.role == 'merchant' and store_id:
            return StockReceive.objects.filter(
                inventory_item__store_id=store_id,
                inventory_item__store__owner=user,
                payment_status=StockReceive.PaymentStatus.UNPAID
            )
        return StockReceive.objects.none()

class PaySupplierView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("=== DEBUG: Incoming PaySupplier Request ===")
        print("Raw Request Data:", request.data)

        stock_receive_id = request.data.get('stock_receive_id')
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')

        if not all([stock_receive_id, phone_number, amount]):
            print("ERROR: Missing fields",
                  {"stock_receive_id": stock_receive_id, "phone_number": phone_number, "amount": amount})
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        formatted_phone = format_phone_number(phone_number)
        print("Formatted Phone:", formatted_phone)

        if not formatted_phone:
            print("ERROR: Invalid phone format for:", phone_number)
            return Response({
                "error": f"Invalid phone number format: '{phone_number}'. Please ensure it's like 07... or 254..."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock_receive = StockReceive.objects.get(pk=stock_receive_id)
            print("Found StockReceive:", stock_receive.id)
        except StockReceive.DoesNotExist:
            print("ERROR: StockReceive not found:", stock_receive_id)
            return Response({"error": "Delivery record not found."}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(stock_receive, 'mpesa_transaction'):
            transaction = stock_receive.mpesa_transaction
            print("Existing Transaction Status:", transaction.status)
            if transaction.status == MpesaTransaction.Status.SUCCESS:
                return Response({"error": "Already paid."}, status=status.HTTP_400_BAD_REQUEST)
            if transaction.status == MpesaTransaction.Status.PENDING:
                return Response({"error": "Payment already pending."}, status=status.HTTP_400_BAD_REQUEST)

        callback_url = "https://b78a2588706c.ngrok-free.app/api/v1/payments/mpesa-callback/"
        print("Callback URL:", callback_url)

        transaction_desc = (f"Pay {stock_receive.inventory_item.name}")[:13]

        mpesa_response = lipa_na_mpesa_online(
            phone_number=formatted_phone,
            amount=int(float(amount)),
            account_reference=f"STORE{stock_receive.inventory_item.store.id}",
            transaction_desc=transaction_desc,
            callback_url=callback_url
        )
        print("M-Pesa API Response:", mpesa_response)

        checkout_request_id = mpesa_response.get('CheckoutRequestID')
        if not checkout_request_id:
            print("ERROR: No CheckoutRequestID in response.")
            return Response({"error": "Failed to initiate M-Pesa STK push. Check Daraja credentials."}, status=status.HTTP_400_BAD_REQUEST)

        MpesaTransaction.objects.create(
            stock_receive=stock_receive,
            amount=amount,
            checkout_request_id=checkout_request_id
        )
        print("Transaction Created Successfully")

        return Response(mpesa_response, status=status.HTTP_200_OK)

class MpesaCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print("M-Pesa Callback Received:", request.data)
        return Response(status=status.HTTP_200_OK)

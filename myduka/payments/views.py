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
        stock_receive_id = request.data.get('stock_receive_id')
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')

        if not all([stock_receive_id, phone_number, amount]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        formatted_phone = format_phone_number(phone_number)
        if not formatted_phone:
            return Response({
                "error": f"Invalid phone number format: '{phone_number}'. Please ensure the supplier's number is correct and in a valid format (e.g., 07... or 254...)."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock_receive = StockReceive.objects.get(pk=stock_receive_id)
        except StockReceive.DoesNotExist:
            return Response({"error": "Delivery record not found."}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(stock_receive, 'mpesa_transaction'):
            transaction = stock_receive.mpesa_transaction
            if transaction.status == MpesaTransaction.Status.SUCCESS:
                return Response({"error": "This delivery has already been successfully paid for."}, status=status.HTTP_400_BAD_REQUEST)
            if transaction.status == MpesaTransaction.Status.PENDING:
                 return Response({"error": "A payment for this delivery is already pending. Please check M-Pesa."}, status=status.HTTP_400_BAD_REQUEST)
        
        callback_url = "https://2e0e9bc3d0c2.ngrok-free.app/api/v1/payments/mpesa-callback/"
        
        try:
            mpesa_response = lipa_na_mpesa_online(
                phone_number=formatted_phone,
                amount=int(float(amount)),
                account_reference=f"STORE{stock_receive.inventory_item.store.id}",
                transaction_desc=f"Payment for {stock_receive.inventory_item.name}",
                callback_url=callback_url
            )
        except Exception as e:
            print("--- MPESA API ERROR ---")
            print(f"An exception occurred: {e}")
            print("--- END MPESA API ERROR ---")
            return Response({"error": "An error occurred while contacting the M-Pesa API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        checkout_request_id = mpesa_response.get('CheckoutRequestID')
        if not checkout_request_id:
            print("--- MPESA API ERROR ---")
            print(f"Safaricom API returned an error: {mpesa_response}")
            print("--- END MPESA API ERROR ---")
            return Response({"error": "Failed to initiate M-Pesa STK push. Check Daraja credentials."}, status=status.HTTP_400_BAD_REQUEST)

        MpesaTransaction.objects.create(
            stock_receive=stock_receive,
            amount=amount,
            checkout_request_id=checkout_request_id
        )

        return Response(mpesa_response, status=status.HTTP_200_OK)


class MpesaCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print("M-Pesa Callback Received:", request.data)
        return Response(status=status.HTTP_200_OK)

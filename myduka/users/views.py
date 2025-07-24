# =======================================================================
# FILE: myduka/users/views.py (FIXED)
# =======================================================================
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User
from .serializers import UserSerializer, RegisterSerializer, InviteSerializer, CompleteInviteSerializer
from .permissions import IsMerchant, IsAdmin
from .utils import send_invite_email
from stores.models import Store

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class InviteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMerchant | IsAdmin]

    def post(self, request, *args, **kwargs):
        serializer = InviteSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            role = serializer.validated_data['role']
            store_id = serializer.validated_data.get('store_id')
            inviter = request.user

            target_store = None

            if inviter.role == User.Role.MERCHANT:
                if role != User.Role.ADMIN:
                    return Response({'error': 'Merchants can only invite Admins.'}, status=status.HTTP_403_FORBIDDEN)
                if not store_id:
                    return Response({'error': 'A store_id is required when inviting an Admin.'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    target_store = Store.objects.get(pk=store_id, owner=inviter)
                except Store.DoesNotExist:
                    return Response({'error': 'Store not found or you are not the owner.'}, status=status.HTTP_404_NOT_FOUND)
            
            elif inviter.role == User.Role.ADMIN:
                if role != User.Role.CLERK:
                    return Response({'error': 'Admins can only invite Clerks.'}, status=status.HTTP_403_FORBIDDEN)
                target_store = inviter.store
                if not target_store:
                     return Response({'error': 'Admin is not assigned to a store.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={'username': email, 'role': role, 'is_active': False}
                )
                if not created and user.is_active:
                    return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

                user.store = target_store
                user.save()

                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                invite_link = f"http://localhost:5173/invite/{access_token}"

                send_invite_email(email, invite_link)

                return Response({'message': f'Invite sent to {email}.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompleteInviteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CompleteInviteSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                user = User.objects.get(pk=user_id)

                if user.is_active:
                    return Response({'error': 'This invitation has already been used.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(password)
                user.is_active = True
                user.save()

                return Response({'message': 'Account activated successfully!'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManageStaffView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMerchant]

    def patch(self, request, user_id, *args, **kwargs):
        merchant = request.user
        try:
            staff_member = User.objects.get(pk=user_id, store__owner=merchant)
            is_active = request.data.get('is_active')
            if is_active is not None:
                staff_member.is_active = is_active
                staff_member.save()
                return Response({'status': 'User status updated'}, status=status.HTTP_200_OK)
            return Response({'error': 'is_active flag not provided'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found in your stores."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id, *args, **kwargs):
        merchant = request.user
        try:
            staff_member = User.objects.get(pk=user_id, store__owner=merchant)
            staff_member.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found in your stores."}, status=status.HTTP_404_NOT_FOUND)

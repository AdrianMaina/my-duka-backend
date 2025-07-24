# =======================================================================
# FILE: myduka/users/serializers.py (FIXED)
# =======================================================================
from rest_framework import serializers
from .models import User
from stores.models import Store # Corrected import

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'store']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        user.role = User.Role.MERCHANT
        user.save()
        return user

class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=[User.Role.ADMIN, User.Role.CLERK])
    store_id = serializers.IntegerField(required=False)

class CompleteInviteSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

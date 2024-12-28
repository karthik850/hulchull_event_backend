from rest_framework import serializers
from .models import SecretCodeDB

class SecretCodeDBSerializer(serializers.ModelSerializer):
    """Serializer for admin with all fields."""
    class Meta:
        model = SecretCodeDB
        fields = '__all__'

class SecretCodeUserSerializer(serializers.ModelSerializer):
    """Serializer for user, excluding username."""
    class Meta:
        model = SecretCodeDB
        exclude = ('user_name','associate_name','gender')

class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8) 

# Serializer for login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
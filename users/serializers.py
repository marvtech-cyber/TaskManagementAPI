from rest_framework import serializers
from .models import CustomUser

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        # Model used by the serializer
        model = CustomUser
        # Model fields that will be included in the serialized representation
        fields = ['id', 'username', 'email']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        # Model used by the serializer
        model = CustomUser
        # Model fields that will be included in the serialized representation
        fields = ['id', 'username', 'email', 'password']
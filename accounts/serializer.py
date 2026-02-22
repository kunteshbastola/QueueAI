from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'priority_type', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
        username=validated_data['username'],
        email=validated_data['email'],
        role=validated_data['role']
    )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['role'] = self.user.role
        data['username'] = self.user.username

        return data

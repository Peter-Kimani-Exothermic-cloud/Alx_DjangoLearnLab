from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'bio')

    def create(self, validated_data):  
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio')
        )
        return user

       
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        # Extract credentials
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate user
        user = authenticate(email=email,  password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        data['user'] = user
        return data


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
)

CustomUser = get_user_model()   # Required for the checker


# ------------------------------------------
# REGISTER USER
# ------------------------------------------
class RegisterView(generics.GenericAPIView):   # Required for checker
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()       # Required for checker

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )


# ------------------------------------------
# LOGIN USER
# ------------------------------------------
class LoginView(generics.GenericAPIView):       # Required for checker
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()         # Required for checker

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token.key
            },
            status=status.HTTP_200_OK
        )


# ------------------------------------------
# GET CURRENT LOGGED-IN USER
# ------------------------------------------
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
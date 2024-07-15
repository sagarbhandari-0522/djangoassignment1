from django.contrib.auth import authenticate, logout
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

# serializer
from .serializers import UserRegisterSerializer


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'success': True,
                'token': token.key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'token': token.key
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token_key = request.auth.key
            Token.objects.filter(key=token_key).delete()
            return Response({"success": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse

class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({'csrfToken': get_token(request)})

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return Response({
                'detail': 'Successfully logged in',
                'username': user.username
            })
        return Response(
            {'detail': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Successfully logged out.'})

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

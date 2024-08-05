from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import create_username, is_valid_email

class Signup(APIView):
    def get(self, request):
        return Response({"message": "Signup view"})

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({'message': 'Email or password cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not is_valid_email(email):
            return Response({'message': 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(email=email).exists():
            user = User(
                username = create_username(),
                email = email
                )
            user.set_password(password)
            user.save()
            token = Token.objects.create(user=user)
            response = {
                'message': 'User created successfully',
                'token': token.key
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def get(self, request):
        return Response({"message": "Login view"})

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return Response({'message': 'Email or password cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, email=email, password=password)
        if user:
            token, create = Token.objects.get_or_create(user=user)
            response = {
                'message': 'Login successful',
                'token': token.key
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response({'message': 'Username or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
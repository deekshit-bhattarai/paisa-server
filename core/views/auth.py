import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import (
    ALGORITHM,
    SECRET_KEY,
    generate_access_jwt_token,
    generate_refresh_jwt_token,
)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            access_token = generate_access_jwt_token(user)
            refresh_token = generate_refresh_jwt_token(user)
            return Response({'access_token' : access_token, 'refresh_token' : refresh_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error' : 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data['refresh_token']

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
            if payload.get('type') != 'refresh':
                return Response({'error':'Invalid token type'}, status=status.HTTP_400_BAD_REQUEST)
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            access_token = generate_access_jwt_token(user)
            return Response({'access_token' : access_token}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            raise Response({'error' : 'Refrsh token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            raise Response({'error' : 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



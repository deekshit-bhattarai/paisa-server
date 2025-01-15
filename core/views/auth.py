from core.models import BlacklistedTokens
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.utils import (
    ALGORITHM,
    SECRET_KEY,
    generate_access_jwt_token,
    generate_refresh_jwt_token,
)


class LoginView(APIView):
    """
    This view is used to login the user
    """
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

class LogOutView(APIView):
    """
    Logout currently logged in user

    Attributes:
        authentication_classes(list):Specify authentication class for the view
        permission_classes(list):Specify permission class for view
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        access_token = request.data.get('access_token')
        print(refresh_token)
        breakpoint()
        if not refresh_token:

            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)

            if payload['type'] != 'refresh':
                return Response({'error' : 'Please provide a refresh token'}, status=status.HTTP_400_BAD_REQUEST)

            # user_id = payload['user_id']
            # user = User.objects.get(id=user_id)

            BlacklistedTokens.objects.create(token=[refresh_token, access_token])
            return Response({'success':'User logged out successfully'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error' : 'Refresh token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'error' : "invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error' : "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise Response(str(e))

class RefreshTokenView(APIView):
    """
    Generate new access token if previous one has expired
    """
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

        except Exception as e:
            return Response(str(e))

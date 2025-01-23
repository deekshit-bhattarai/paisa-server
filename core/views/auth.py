from core.mixins import CustomResponseMixin
from core.models import BlacklistedTokens
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from core import core_serializers

from core.utils import (
    ALGORITHM,
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRATION_SECONDS ,
    REFRESH_TOKEN_EXPIRATION_SECONDS,
    generate_access_jwt_token,
    generate_refresh_jwt_token,
)

class UserRegistrationView(CustomResponseMixin, APIView):
    permission_classes = [AllowAny]
    serializer_class = core_serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        print("registering user")
        serializer = self.serializer_class(data=request.data)
        print(f"The serializer is : { serializer }")
        if serializer.is_valid():
            serializer.save()
            return self.return_response(
                success=True,
                message="User registered successfully",
                status = status.HTTP_201_CREATED
            )
        return self.return_response(
            success = False,
            message = "User cannot be registed",
            errors = serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )


class LoginView(CustomResponseMixin, APIView):
    """
    This view is used to login the user
    """
    def post(self, request):
        print(f"LoginView {request}")
        try:
            username = request.data['username']
            password = request.data['password']

            user = authenticate(username=username, password=password)
            print(f"Login user {user}")

            if user:
                access_token = generate_access_jwt_token(user)
                refresh_token = generate_refresh_jwt_token(user)
                response = Response({'message' : 'Login Successful'})
                response.set_cookie("access_token", access_token, httponly=True, samesite="strict", max_age=ACCESS_TOKEN_EXPIRATION_SECONDS)
                response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="strict", max_age=REFRESH_TOKEN_EXPIRATION_SECONDS)
                print(f"Login response is : {response}")
                return self.return_response(
                    success=True,
                    message="User logged in successfully",
                    data={"access_token" : access_token, "refresh_token" : refresh_token},
                    status=status.HTTP_200_OK
                )
            response = Response()
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return self.return_response(
                success=False,
                message="Invalid credentials",
                errors = {"detail" : "Invalid username or password"},
                status = status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.return_response(
                success=False,
                message="An error occured while logging in",
                errors = {"detail" : str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

class LogOutView(CustomResponseMixin, APIView):
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
        if not refresh_token:

            return self.return_response(
                success=False,
                message="No refresh token provided",
                errors= {"error" : "Refresh token is required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)

            if payload['type'] != 'refresh':
                return self.return_response(
                    success=False,
                    message="Token type is not refresh token",
                    errors= {"error" : "Please provide refresh token"},
                    status = status.HTTP_400_BAD_REQUEST
                )

            # user_id = payload['user_id']
            # user = User.objects.get(id=user_id)

            BlacklistedTokens.objects.create(token=[refresh_token, access_token])

            response = Response()
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return self.return_response(
                success=True,
                message="User logged out successfully",
                status = status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return self.return_response(
                success=False,
                message="Expired signature token",
                errors= {"error" : "JWT token signature has expired"},
                status = status.HTTP_400_BAD_REQUEST
            )
        except jwt.InvalidTokenError:
            return self.return_response(
                success=False,
                message="Provided token is invalid",
                errors= {"error" : "The token provided is invalid"},
                status = status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return self.return_response(
                success=False,
                message="No user exists",
                errors= {"error" : "Requested user doens't exixt"},
                status = status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return self.return_response(
                success=False,
                message="An exception was encounterd",
                errors= {"error" : str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

class RefreshTokenView(CustomResponseMixin, APIView):
    """
    Generate new access token if previous one has expired
    """
    def post(self, request):
        refresh_token = request.data['refresh_token']

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
            if payload.get('type') != 'refresh':
                return self.return_response(
                    success=False,
                    message = "Invalid token type",
                    errors = {"error" : "Invalid token type"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            access_token = generate_access_jwt_token(user)
            return self.return_response(
                success=True,
                message = "Token generated successfully",
                data = {'access_token' : access_token},
                status = status.HTTP_200_OK
            )

        except Exception as e:
            return self.return_response(
                success=False,
                message="An exception was encounterd",
                errors= {"error" : str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

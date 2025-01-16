from datetime import datetime, timedelta
from itertools import chain

import jwt
from django.conf import settings
from django.db import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from core.models import ExpenseTracker, IncomeTracker

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_SECONDS = 86400
REFRESH_TOKEN_EXPIRATION_SECONDS = 432000

def generate_access_jwt_token(user):
    """
    Generate access JWT for given user
    """
    expiration = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRATION_SECONDS)
    payload = {
        'user_id' : user.id,
        'username': user.username,
        'iat': datetime.utcnow(),
        'exp' : expiration,
        'type' : 'access'

    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def generate_refresh_jwt_token(user):
    """
    Generate JWT token

    :param user [user]: Specifies which user is asking to generate JWT token
    """
    expiration = datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_EXPIRATION_SECONDS)
    payload = {
        'user_id' : user.id,
        'username': user.username,
        'iat': datetime.utcnow(),
        'exp' : expiration,
        'type' : 'refresh'

    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token provided")

def authenticate(request):
    print("Here is authenticate")
    return True


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("Hello from authenticate")
        # Get token from Authorization header (format: "Bearer <token>")
        token = self.get_token_from_request(request)
        if not token:
            return None  # No token, proceed without authentication

        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
            print("Decoded Payload:", payload)  # Print payload for debugging

            # Extract user_id from the decoded payload
            user_id = payload.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('User ID missing in token payload')
            
            # Retrieve user from the database using user_id
            user = self.get_user(user_id)
            return (user, token)  # Return a tuple of (user, token)
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

    def get_token_from_request(self, request):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        print(f'Auth header is : {auth_header}')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]  # Return the token part
        return None

    def get_user(self, user_id):
        # Retrieve the user from the database based on user_id
        from django.contrib.auth.models import User
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')


def current_balance(user):
    income =  ( IncomeTracker.objects.filter(user=user).aggregate(models.Sum("amount"))["amount__sum"] or 0 ) 
    expense = ( ExpenseTracker.objects.filter(user=user).aggregate(models.Sum("amount"))["amount__sum"] or 0)

    current_balance = income - expense
    return {
        'current_balance' : current_balance,
        'total_income' : income,
        'total_expense' : expense
    }


def all_transactions(user):

    income_transactions = IncomeTracker.objects.filter(user=user).values(
        'amount', 'source', 'reason',  'remarks', 'time'
    ).annotate(transaction_type=models.Value('Income', output_field=models.CharField()))

    expense_transactions = ExpenseTracker.objects.filter(user=user).values(
        'amount', 'source', 'reason', 'category', 'remarks', 'time'
    ).annotate(transaction_type=models.Value('Expense', output_field=models.CharField()))

    # Combine and sort by time
    recent_transactions = sorted(
        chain(income_transactions, expense_transactions),
        key=lambda x: x['time'],
        reverse=True
    )
    return {
        'recent_transactions' : recent_transactions[:5],
        'all_transactions' : recent_transactions,
        'income_table': income_transactions,
        'expense_table' : expense_transactions
    }

from datetime import datetime, timedelta

import jwt
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_SECONDS = 3600
REFRESH_TOKEN_EXPIRATION_SECONDS = 604800

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
    Generate refresh JWT for given user
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


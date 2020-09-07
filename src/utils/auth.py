"""
    Token-based authentication
"""

from flask import current_app
import jwt
from datetime import datetime, timedelta
import bcrypt

SECRET_KEY = current_app.config["SECRET_KEY"]

def encode_token(user_phone_num: str) -> str:
    """ Generate JWT string """
    try:
        payload = {
            # expire after 3 hours
            "exp": datetime.utcnow() + timedelta(minutes=5),
            # issued at
            "iat": datetime.utcnow(),
            # identification data
            "sub": user_phone_num,
        }

        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        return e


def decode_token(jwt_str: str) -> str | (str, int):
    """ Decode JWT string to get user's identification data """
    try:
        payload = jwt.decode(jwt_str, SECRET_KEY)
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        # HTTP response code 401: unauthorised
        return "Your authentication token is expired. Please re-login!", 401
    except jwt.InvalidTokenError:
        # HTTP response code 409: conflict with server's tracking of the resource
        return (
            "There's something wrong with your authentication token. Please re-login!",
            409,
        )


def hash_password(pwd: str) -> str:
    return bcrypt.hashpw(password=pwd, salt=bcrypt.gensalt())

# Don't get confused!!! `check_password` behaves identically to `bcrypt.checkpw`
# (╯°□°）╯︵ ┻━┻
check_password = bcrypt.checkpw


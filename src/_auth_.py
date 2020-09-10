from flask import current_app
import bcrypt
from jwt import ExpiredSignatureError, InvalidTokenError
from flask_jwt_extended import (
    decode_token as _decode_token,
    create_access_token
)
from datetime import datetime, timedelta

""" This module contains utility functions regarding `bcrypt` encryption """

""" (1) `bcrypt` encryption """
# SECRET_KEY = current_app.config["JWT_SECRET_KEY"]
SALT = bcrypt.gensalt()

def hash_password(pwd: str) -> str:
    # `pwd` is an UTF-8 string, whereas `bcrypt.hasspwd` requires a bytes 
    hashed_bytes = bcrypt.hashpw(password=str.encode(pwd), salt=SALT)
    # returned result need to be an UTF-8 string
    return hashed_bytes.decode()


def check_password(pwd: str, hashed: str) -> bool: 
    # Don't get confused!!! `check_password` behaves identically to `bcrypt.checkpw`
    # (╯°□°）╯︵ ┻━┻
    pwd_bytes    = str.encode(pwd)
    hashed_bytes = str.encode(hashed)
    return bcrypt.checkpw(password=pwd_bytes, hashed_password=hashed_bytes)

""" END: (1) `bcrypt` encryption """

""" (2) customised JWT utility methods """

"""
    Default configuration options (configurable using environmental variables):
    - `JWT_HEADER_NAME`    = "Authorization"
    - `JWT_HEADER_TYPE`    = "Bearer"
    - `JWT_TOKEN_LOCATION` = ["header"]

    @Reference https://flask-jwt-extended.readthedocs.io/en/stable/options/
"""


def encode_token(user_phone_num: str) -> str:
    """ 
        Customised utility function built on top of `flask_jwt_extended.create_access_token` 
        to generate JWT string 

        :return: An encoded access token 
    """

    exp = timedelta(minutes=5)
    try:
        return create_access_token(identity=user_phone_num, expires_delta=exp)
    except Exception as e:
        return str(e)


def decode_token(jwt_str: str):
    """ 
        Customised utility function built on top of `flask_jwt_extended.decode_token` 
        to decoded JWT string

        :returns: either tuple of token dictionary & number 200 or tuple of ("error message", HTTP code)
    """
    try:
        jwt_claim = _decode_token(encoded_token=jwt_str, allow_expired=True)
        return jwt_claim, 200
    except ExpiredSignatureError:
        # HTTP response code 401: unauthorised
        return "Your authentication token is expired. Please re-login!", 401
    except InvalidTokenError:
        # HTTP response code 409: conflict with server's tracking of the resource
        return (
            "There's something wrong with your authentication token. Please re-login!",
            409,
        )


""" END: (2) customised JWT utility methods """

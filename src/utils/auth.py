"""
    Token-based authentication

    @TODO 
        - migrate to flask-jwt-extended
        @ref https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
"""

from flask import current_app
import jwt
from datetime import datetime, timedelta
import bcrypt

# SECRET_KEY = current_app.config["JWT_SECRET_KEY"]
SALT = bcrypt.gensalt()

""" JWT """

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


def decode_token(jwt_str: str):
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

""" `bcrypt` encryption """

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

if __name__ == "__main__": 
    # for pwd in [f"aacc123{i}" for i in range(4, 7)]: 
    #     print(hash_password(pwd))
    """ 
        a raw password string can be hashed into different strings
        but each hashed string can refer to only one identical raw password string
    """
    


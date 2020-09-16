from base64 import b64decode, b64encode
from flask import request as req, jsonify
from pymongo import MongoClient, ReturnDocument
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_raw_jwt,
)
from datetime import timedelta
from logzero import logger  # console logger

from .utils import check_password, hash_password, encode_token, decode_token, atob

"""
    Define authentication routes
"""


def _suppliment_login_route(cur_app):
    """
        Suppliment login route to the given Flask app object

        :param: `cur_app`: <class 'flask.app.Flask'>
    """

    DB_URI = cur_app.config["DATABASE_URI"]
    DB_NAME = cur_app.config["DATABASE_NAME"]

    @cur_app.route("/auth/login", methods=["GET"])
    def handle_login():
        """
            Extract login credentials from BasicAuth request header,
            
            :return: JWT access token if user is successfully logged in
        """
        try:
            # basic_auth = f"Bearer {encoded_credentials}"
            basic_auth = req.headers.get("Authorization")
            encoded_credentials = basic_auth.split("Basic ")[1]
            # decoded_credentials = f"{PHONE}:{RAW_PASSWORD}"
            decoded_credentials = atob(encoded_credentials)
            PHONE, RAW_PASSWORD = decoded_credentials.split(":")

            logger.info(f"original credential string: {encoded_credentials}")
            """ validation """
            for field in [PHONE, RAW_PASSWORD]:
                if field is None:
                    # HTTP response code 400: bad request ¯\_(ツ)_/¯
                    return (
                        jsonify(
                            {"message": "Important fields are missing. Please re-check!"}
                        ),
                        400,
                        {"Content-Type": "application/json"},
                    )

            """ authenticate """
            client = MongoClient(host=DB_URI)
            db = client[DB_NAME]
            user_col = db["user"]
            # get user
            user_doc = user_col.find_one({"Phone": PHONE})

            if user_doc is None:
                # HTTP response code 400: bad request ¯\_(ツ)_/¯
                return (
                    jsonify(
                        {
                            "message": "Your login credentials are incorrect. Please re-check!"
                        }
                    ),
                    400,
                    {"Content-Type": "application/json"},
                )

            else:
                user_hashed_pwd = user_doc["Password"]
                if user_hashed_pwd is None:
                    logger.info("Connection with database is down.")
                    # HTTP response code 500: internal server error (❍ᴥ❍ʋ)
                    return jsonify({"message": "Internal server error!"}), 500

                if check_password(RAW_PASSWORD, user_hashed_pwd):
                    # generate token string, in which `PHONE` is used as identification data
                    token = create_access_token(
                        identity=PHONE, expires_delta=timedelta(minutes=15)
                    )
                    logger.info(f"Token generated: {token}")
                    # HTTP response code 201, ~(˘▾˘~) of which body contains a generated JWT code (~˘▾˘)~
                    return jsonify({"jwt": token}), 201, {"Content-Type": "application/json"}
        except (RuntimeError, TypeError, NameError) as e: 
            logger.error(str(e))
            return jsonify({"msg": "Internal server error"}), 500, {"Content-Type": "application/json"}


def _suppliment_logout_route(cur_app):
    """
        Suppliment logout route to the given Flask app object

        :param: `cur_app`: <class 'flask.app.Flask'>
    """

    DB_URI = cur_app.config["DATABASE_URI"]
    DB_NAME = cur_app.config["DATABASE_NAME"]

    @cur_app.route("/auth/logout", methods=["POST"])
    @jwt_required
    def handle_logout():
        """ 
            Revoke user's current access token
    
            This kind of request is POST because they are not necessarily idempotent 
        """
        # get the JWT token's ID
        jti = get_raw_jwt()["jti"]
        # get the list of blacklisted tokens in database
        db_client = MongoClient(DB_URI)
        db = db_client[DB_NAME]
        blacklist_col = db["token_blacklist"]
        # push `jti` to the list persisted in database
        returned_doc = blacklist_col.find_one_and_update(
            filter={},
            update={"$push": {"List": str(jti)}},
            return_document=ReturnDocument.AFTER,
        )

        if returned_doc is not None:
            logger.info("Logout request successfully handled.")
            # HTTP response code 200: request succeeded
            return jsonify({"message": "Successfully logged out!"}), 200, {"Content-Type": "application/json"}
        else:
            logger.info("Connection with database is down.")
            # HTTP response code 500: internal server error (❍ᴥ❍ʋ)
            return jsonify({"message": "Internal server error!"}), 500, {"Content-Type": "application/json"}


def _suppliment_register_route(cur_app):
    """
        Suppliment register route to the given Flask app object

        :param: `cur_app`: <class 'flask.app.Flask'>
    """
    DB_URI = cur_app.config["DATABASE_URI"]
    DB_NAME = cur_app.config["DATABASE_NAME"]

    @cur_app.route("/auth/register", methods=["POST"])
    def handle_register():
        FULL_NAME = req.json.get("full_name")
        PHONE = req.json.get("phone")
        EMAIL = req.json.get("email")
        RAW_PASSWORD = req.json.get("password")
        ROLE = req.json.get("role")
        LICENSE_KEY = req.json.get("license_key")

        """ validation """
        for field in [FULL_NAME, PHONE, EMAIL, RAW_PASSWORD, LICENSE_KEY]:
            if field is None:
                # HTTP response code 400: bad request ¯\_(ツ)_/¯
                return (
                    {"message": "Important fields are missing. Please re-check!"},
                    400,
                )

        """ check if there is an user with this profile information already existed """
        client = MongoClient(host=DB_URI)
        db = client[DB_NAME]
        user_col = db["user"]

        query_filter = {
            "$or": [{"FullName": FULL_NAME}, {"Phone": PHONE}, {"Email": EMAIL}]
        }
        # oops, did I forget to check if there is an user having
        # the same password witht the submited one? (づ￣ ³￣)づ
        dupl_user = user_col.find_one(query_filter)

        if dupl_user is not None:
            # HTTP response code 409: request is in conflict with server's resources ｡゜(｀Д´)゜｡
            return {"message": "This user already existed. Forgot password?"}, 409
        else:
            """ Check validity of the submitted license key """
            bank_col = db["bank"]
            query_filter = {"license_key": LICENSE_KEY}
            bank_doc = bank_col.find_one(query_filter)

            if bank_doc is not None:
                new_user_doc = {
                    "FullName": FULL_NAME,
                    "Phone": PHONE,
                    "Email": EMAIL,
                    "Password": hash_password(RAW_PASSWORD),
                    "Role": ROLE,
                    "BankId": bank_col["BankId"],
                    "BranchId": bank_col["BranchId"],
                }
                db_user_id = user_col.insert_one(new_user_doc).inserted_id

                # HTTP response code 201: ~(˘▾˘~) new resource successfully created (~˘▾˘)~
                return jsonify({"db_user_id": db_user_id}), 201
            else:
                # HTTP response code 403: Forbidden （╯°□°）╯︵( .o.)
                return {"message": "Invalid license key. Please re-check!"}, 403


def supplement_auth_routes(app):
    """
        Suppliment the 3 authentication routes defined above to the given `app`

        :param: `app`: <class 'flask.app.Flask'>
    """
    # JWT management need to be consistent throughout the Flask app

    for suppliment_def in [
        _suppliment_login_route,
        _suppliment_logout_route,
        _suppliment_register_route,
    ]:
        suppliment_def(app)


if __name__ == "__main__":
    pass

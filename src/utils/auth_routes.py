""" 
    Define protected routes 
"""

from flask import Blueprint, request as req, jsonify, current_app as cur_app
from pymongo import MongoClient, ReturnDocument
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt
)
from auth import check_password, hash_password
from models import User

DB_URI = cur_app.config["DATABASE_URI"]
DB_NAME = cur_app.config["DATABASE_NAME"]
SECRET_KEY = cur_app.config["JWT_SECRET_KEY"]

# JWT management need to be consistent throughout the Flask app
# that's why we need to use decorator of `current_app`
@cur_app.route("/auth/login", method = ["POST"])
def handle_login():
    PHONE = req.json.get("phone", None)
    RAW_PASSWORD = req.json.get("password", None)

    """ validation """
    for field in [PHONE, RAW_PASSWORD]:
        if field is None: 
            # HTTP response code 400: bad request ¯\_(ツ)_/¯
            return jsonify({ "message": "Important fields are missing. Please re-check!" }), 400
    
    """ authenticate """
    client = MongoClient(host=DB_URI)
    db = client[DB_NAME]
    user_col = db["user"]
    # get user
    user_doc = db.find_one({ "Phone": PHONE })

    if user_doc is None: 
        # HTTP response code 400: bad request ¯\_(ツ)_/¯
        return jsonify({ "message": "Requested user not existed. Please re-check!" }), 400
    else:
        user_hashed_pwd = user_doc["Password"]
        if user_hashed_pwd is None: 
            # HTTP response code 500: internal server error (❍ᴥ❍ʋ)
            return jsonify({ "message": "Internal server error!" }), 500 
        
        if (check_password(RAW_PASSWORD, user_hashed_pwd)): 
            # generate token string, in which `PHONE` is used as identification data
            token = create_access_token(identity=PHONE)
            # HTTP response code 201, ~(˘▾˘~) of which body contains a generated JWT code (~˘▾˘)~
            return jsonify({ "jwt": token }), 201 

@cur_app.route("/auth/logout", method = ["POST"])
@jwt_required
def handle_logout():
    """ 
        Revoke user's current access token

        This kind of request is POST because they are not necessarily idempotent 
    """
    # get the JWT token's ID
    jti = get_raw_jwt()["jti"]
    # get the list of blacklisted tokens in database
    db_client = MongoClient(app.config["DATABASE_URI"])
    db = db_client[app.config["DATABASE_NAME"]]
    blacklist_col = db["token_blacklist"]
    # push `jti` to the list persisted in database
    returned_doc = blacklist_col.find_one_and_update(
        filter={},
        update={
            "$push": {
                "List": str(jti)
            }
        }
        return_document=ReturnDocument.AFTER
    )

    if returned_doc is not None:
        # HTTP response code 200: request succeeded
        return { "message": "Successfully logged out!" }, 200
    else: 
        # HTTP response code 500: internal server error (❍ᴥ❍ʋ)
        return { "message": "Internal server error!"}, 500


@cur_app.route("/auth/register", method = ["POST"])
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
            return jsonify({ "message": "Important fields are missing. Please re-check!" }), 400
        
    """ check if there is an user with this profile information already existed """
    client = MongoClient(host=DB_URI)
    db = client[DB_NAME]
    user_col = db["user"]

    query_filter = {
        "$or": [
            { "FullName": FULL_NAME }, 
            { "Phone": PHONE }, 
            { "Email": EMAIL }
        ]
    }
    # oops, did I forget to check if there is an user having 
    # the same password witht the submited one? (づ￣ ³￣)づ 
    dupl_user = user_col.find_one(query_filter)

    if dupl_user is not None:
        # HTTP response code 409: request is in conflict with server's resources ｡゜(｀Д´)゜｡
        return jsonify({ "message": "This user already existed. Forgot password?" }), 409
    else: 
        """ Check validity of the submitted license key """
        bank_col = db["bank"]
        query_filter = { "license_key": LICENSE_KEY }
        bank_doc = bank_col.find_one(query_filter)
        
        if bank_doc is not None:
            new_user_doc = {
                "FullName": FULL_NAME, 
                "Phone": PHONE,
                "Email": EMAIL,
                "Password": hash_password(RAW_PASSWORD), 
                "Role": ROLE,
                "BankId": bank_col["BankId"],
                "BranchId": bank_col["BranchId"]
            }
            db_user_id = user_col.insert_one(new_user_doc).inserted_id

            # HTTP response code 201: ~(˘▾˘~) new resource successfully created (~˘▾˘)~
            return jsonify({ "db_user_id": db_user_id }), 201
        else: 
            # HTTP response code 403: Forbidden （╯°□°）╯︵( .o.)
            return jsonify({ "message": "Invalid license key. Please re-check!" }), 403

if __name__ == "__main__":
    print(hash_password("aacc1236"))
    """
        @TODO 
            - check if submitted key is expired yet
    """
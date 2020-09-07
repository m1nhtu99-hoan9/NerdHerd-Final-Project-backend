from flask import Blueprint, request as req, jsonify, current_app as cur_app
from pymongo import MongoClient
from auth import check_password, hash_password
from models import User

DB_URI = cur_app.config["DATABASE_URI"]
DB_NAME = cur_app.config["DATABASE_NAME"]

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/auth/login", method = ["POST"])
def handle_login(): 
    
@auth_bp.route("/auth/logout", method = ["DELETE"])
def handle_logout():

@auth_bp.route("/auth/register", method = ["POST"])
def handle_register(): 
    FULL_NAME = req.args.get("full_name")
    PHONE = req.args.get("phone")
    EMAIL = req.args.get("email")
    RAW_PASSWORD = req.args.get("password")
    ROLE = req.args.get("role")
    LICENSE_KEY = req.args.get("license_key")

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
        return { "message": "This user already existed. Forgot password?" }, 409
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
            return { "db_user_id": db_user_id }, 201
        else: 
            # HTTP response code 403: Forbidden （╯°□°）╯︵( .o.)
            return { "message": "Invalid license key. Please re-check!" }, 403

    """
        @TODO 
            - check if submitted key is expired yet
    """
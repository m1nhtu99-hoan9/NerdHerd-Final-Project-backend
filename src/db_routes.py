from pymongo import MongoClient, ReturnDocument
from flask_jwt_extended import jwt_required


def _supplement_crescore_route(app):
    """
        Supplement route to query credit score

        :param: `app`: <class 'flask.app.Flask'>
    """

    DB_URI = cur_app.config["DATABASE_URI"]
    DB_NAME = cur_app.config["DATABASE_NAME"]

    @cur_app.route("/crescore", methods=["GET"])
    @jwt_required
    def query_crescore():
        """ Check access token """
        # `get_jwt_identity` decodes JWT in "Authorization" header of the request,
        #  decode it and then return the identity (which is current app's user phone number)
        #  @see `auth/jwt` module; `app` module
        user_phone = get_jwt_identity()
        if user_phone is None:
            # HTTP response code 401: unauthorised
            return {"message": "Unauthorised access! Please re-login! "}, 401

        """ Proceed with the request to get credit score """
        # get customer's phone number from HTTP URL parameters
        req_phone = req.args.get("phone")
        if req_phone is None:
            # HTTP response code 400
            return (
                jsonify(
                    {"message": "Invalid request! Please specify the phone number!"}
                ),
                400,
            )
        else:
            # query database to get requested phone number's credit score
            db_client = MongoClient(host=DB_URI)
            db = db_client[DB_NAME]
            customer_col = db["customer"]
            user_col = db["user"]

            if customer_col is None: 
                # HTTP response code 500: internal server error
                return { "message": "Unable to connect with the database" }, 500
            else: 
                customer_doc = customer_col.find_one({ "Phone": req_phone })

                # add requested phone number to current user's search history
                user_col.update_one(
                    filter={"Phone": user_phone}
                    update={"$push": {"SearchHistory": req_phone}}
                )

                # HTTP response code 200
                return { "score": customer_doc["CreditScore"] }, 200
            
def _supplement_profile_route(app): 
    """
        Supplement route to get current user's profile

        :param: `app`: <class 'flask.app.Flask'>
    """

    DB_URI = cur_app.config["DATABASE_URI"]
    DB_NAME = cur_app.config["DATABASE_NAME"]

    @cur_app.route("/profile", methods=["GET"])
    @jwt_required
    def query_crescore():
        """ Check access token """
        # `get_jwt_identity` decodes JWT in "Authorization" header of the request,
        #  decode it and then return the identity (which is current app's user phone number)
        #  @see `auth/jwt` module; `app` module
        user_phone = get_jwt_identity()
        if user_phone is None:
            # HTTP response code 401: unauthorised
            return {"message": "Unauthorised access! Please re-login!"}, 401

        """ Proceed with the request to get user's profile """
        # get customer's phone number from HTTP URL parameters
    
        # query database to get requested phone number's credit score
        db_client = MongoClient(host=DB_URI)
        db = db_client[DB_NAME]
        user_col = db["user"]
        
        if user_col is None: 
            # HTTP response code 500: internal server error
            return { "message": "Unable to connect with the database" }, 500
        else: 
            user_doc = user_col.find_one({ "Phone": user_phone })
            # HTTP response code 200
            return { 
                "phone": user_phone,
                "full_name": user_doc["FullName"],
                "bank_id": user_doc["BankID"],
                "user_id": user_doc["UID"],
                "email": user_doc["Email"]
                "search_history": user_doc["SearchHistory"]
            }, 200

def supplement_db_routes (app): 
    """
        Supplement these 2 above routes into the current Flask app

        :param: `app`: <class 'flask.app.Flask'>
    """
    _supplement_crescore_route(app)
    _supplement_profile_route(app)
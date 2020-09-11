from flask import request as req, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from requests_futures.sessions import FuturesSession
from .api import send_otp_message

f_session = FuturesSession() # to be consumed by `send_otp_message` function call

def supplement_otp_routes(cur_app):
    """
        Supplement OTP routes to the given Flask app object

        :param: `cur_app`: <class 'flask.app.Flask'> 
    """
    
    @cur_app.route("/otp", methods=["GET"])
    @jwt_required
    def get_otp(): 
        """ Check access token """
        # `get_jwt_identity` decodes JWT in "Authorization" header of the request,
        #  decode it and then return the identity (which is current app's user phone number)
        #  @see `auth/jwt` module; `app` module
        user_phone = get_jwt_identity()
        if user_phone is None: 
            # HTTP response code 401: unauthorised 
            return { "message": "Unauthorised access! Please re-login! "}, 401

        """ Proceed with the request for sending OTP confirmation text message """
        # get customer's phone number from HTTP URL parameters
        req_phone = req.args.get("phone")
        if req_phone is None:
            # HTTP response code 400
            return jsonify({ "message": "Invalid request! Please specify the phone number!" }), 400
        else:
            # call the third-party API to send OTP confirmation text message to customer's phone number
            resp_code, otp_code, resp_body = send_otp_message(f_session, req_phone)
            if (resp_code < 300 and resp_code >= 200): 
                # HTTP response code 201 because new OTP is created to be consumed
                return jsonify({ "otp_code": otp_code }), 201
            else:
                # forward the error message received from OTP server
                return jsonify({ "message": jsonify(resp_body) }), 500

"""
TODOs for the next versions: 
    - Limit the number of OTP requests from a phone number in a fix period of time
    - Sanitise phone number string received
"""
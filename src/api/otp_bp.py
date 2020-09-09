from flask import Blueprint, request as req, jsonify
from otp import send_otp_message
from requests_futures.sessions import FuturesSession

otp_bp = Blueprint("otp_bp", __name__)
f_session = FuturesSession() # to be consumed by `send_otp_message` function call

@otp_bp.route("/otp", methods=["GET"])
def get_otp(): 
    phone = req.args.get("phone")
    if phone is None:
        # HTTP response code: 400
        return jsonify({ "message": "Invalid request! Please specify the phone number!" }), 400
    else
        # call the third-party API
        resp_code, otp_code, resp_body = send_otp_message(f_session, phone)
        if (resp_code < 300 and resp_code >= 200): 
            # HTTP response code 201 because new OTP is created to be consumed
            return jsonify({ "otp_code": otp_code }), 201
        else 
            # forward the error message received from OTP server
            return jsonify({ "message": jsonify(resp_body) }), 500

"""
TODOs for the next versions: 
    - Limit the number of OTP requests from a phone number in a fix period of time
    - Sanitise phone number string received
"""
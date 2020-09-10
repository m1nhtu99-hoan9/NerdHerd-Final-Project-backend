from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from logzero import logger
from pymongo import MongoClient
from flask_jwt_extended import JWTManager

from src import supplement_auth_routes, suppliment_otp_routes

from base64 import b64decode, b64encode


def atob(byted_str: str) -> str:
    """ Convert a base-64 encrypted string to decrypted form """
    base64_bytes = byted_str.encode("ascii")
    ascii_bytes = b64decode(base64_bytes)
    return ascii_bytes.decode("ascii")


def create_app():
    """ FLASK APP FACTORY """
    app = Flask(__name__)

    """ intialise configurations """
    app.config.from_object("config.Config")

    """ Setup CORS headers """
    CORS(app)

    """ intialise plugins """
    # flask_jwt_extended need config variable `JWT_SECRET_KEY`
    jwt = JWTManager(app)
    # using MongoDB as centralised storage to persist revoked tokens
    db_client = MongoClient(app.config["DATABASE_URI"])
    db = db_client[app.config["DATABASE_NAME"]]
    blacklist_col = db["token_blacklist"]

    @jwt.token_in_blacklist_loader
    def is_token_in_blacklist(decrypted_token: dict) -> bool:
        """
        This decorator sets the callback function that will be called when
        a protected endpoint is accessed and will check if the JWT has been
        been revoked. By default, this callback is not used.

        See also: `handle_login` from module `auth_routes`

        Reference: https://flask-jwt-extended.readthedocs.io/en/stable/blacklist_and_token_revoking/
        """
        logger.info("Checking if user's token is in the blacklist")
        # get JWT ID from the `dict` argument
        jti = decrypted_token["jti"]
        # retrieve list of blacklisted tokens from database
        blacklist_doc = blacklist_col.find_one()
        blacklist = [str(v) for v in blacklist_doc["List"]]
        return jti in blacklist

    """ Definition of the basic routes. """

    # supplement route definitions to this Flask `app`
    # <!-- not the most professional way to do it but at least I get the job done (；一_一) -->
    supplement_auth_routes(app)
    suppliment_otp_routes(app)

    @app.route("/")
    def hello_world():
        logger.info("/")
        return "Hello World"

    @app.route("/basic_auth")
    def handle_basic_auth():
        # basic_auth = f"Bearer {encoded_credentials}"
        basic_auth = request.headers.get("Authorization")
        encoded_credentials = basic_auth.split("Basic ")[1]
        decoded_creds = atob(encoded_credentials)
        return {"data": decoded_creds, "type": str(type(encoded_credentials))}, 200

    @app.route("/debug/route_list")
    def debug_route_list():
        result = {"url_list": [str(url) for url in app.url_map.iter_rules()]}
        headers = request.headers
        return jsonify({"routes": result, "type_info": {"app": str(type(app))}})

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config["PORT"]

    app.run(host="127.0.0.1", port=port, debug=app.config["DEBUG"])

""" Side notes:
    - In local environment, to import a global config variable (defined in ./venv/bin/activate),
      use `os.environ.get(key={key}, default={default})`
    - Route format `api/username/<userId>`
    - To retrieve a parameter in URI, use `request.args.get("param_key", "default_value")`
"""

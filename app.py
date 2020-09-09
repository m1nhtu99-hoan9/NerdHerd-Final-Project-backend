from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from logzero import logger
from pymongo import MongoClient
from flask_jwt_extended import JWTManager

# from src import list_all_bps


def create_app():
    app = Flask(__name__)

    """ intialise configurations """
    app.config.from_object("config.Config")

    """ Setup CORS headers """
    CORS(app)

    """ intialise plugins """
    # flask_jwt_extended need config variable `JWT_SECRET_KEY`
    jwt = JWTManager(app)
    # using MongoDB as centralised storage to persist revoked tokens
    db_client     = MongoClient(app.config["DATABASE_URI"])
    db            = db_client[app.config["DATABASE_NAME"]]
    blacklist_col = db["token_blacklist"]

    """
        This decorator sets the callback function that will be called when
        a protected endpoint is accessed and will check if the JWT has been
        been revoked. By default, this callback is not used.

        Reference: https://flask-jwt-extended.readthedocs.io/en/stable/blacklist_and_token_revoking/
    """
    @jwt.token_in_blacklist_loader
    def is_token_in_blacklist(decrypted_token: dict) -> bool:
        logger.info("Checking if user's token is in the blacklist")
        # get JWT ID from the `dict` argument
        jti           = decrypted_token["jti"]
        # retrieve list of blacklisted tokens from database
        blacklist_doc = blacklist_col.find_one()
        blacklist     = [ str(v) for v in blacklist_doc["List"] ]
        return jti in blacklist

    """ Definition of the routes. Import all blueprints """
    # for bp in list_all_bps:
    #   app.register_blueprint(bp)

    @app.route("/")
    def hello_world():
        logger.info("/")
        return "Hello World"

    @app.route("/open_db")
    def open_db():
        logger.info("accessing token blacklist")
        db_client = MongoClient(app.config["DATABASE_URI"])
        db = db_client[app.config["DATABASE_NAME"]]
        blacklist_col = db["token_blacklist"]

        blacklist = blacklist_col.find_one()
        token_list = [str(v) for v in blacklist["List"]]
        return {"content": token_list, "dir": str(dir(blacklist)),"env_config_vars": {"DATABASE_NAME": app.config["DATABASE_NAME"]}}

    @app.route("/meta/<info>")
    def fetch_meta(info):
        logger.info(f"/meta/{info}")

        info_dict = {"url_list": app.url_map}
        headers = request.headers
        return jsonify(
            {
                "info": str(info_dict[info]).split("\n"),
                "header": (headers.get("Connection")),
            }
        )

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config["PORT"]
    app.run(host="127.0.0.1", port=port, debug=app.config["DEBUG"])

"""
    - In local environment, to import a global config variable (defined in ./venv/bin/activate),
      use `os.environ.get(key={key}, default={default})`
    - Route format `api/username/<userId>`
    - To retrieve a parameter in URI, use `request.args.get("param_key", "default_value")`
"""

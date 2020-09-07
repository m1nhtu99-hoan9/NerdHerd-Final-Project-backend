"""Flask App Configuration"""

from os import environ as env, path

BASE_DIR = path.abspath(path.dirname(__name__))

class Config: 
    FLASK_APP = env.get("FLASK_APP")
    PORT = int(env.get("PORT", 8000))
    DATABASE_NAME = env.get("DB_NAME")
    DATABASE_URI = env.get("DATABASE_URI")
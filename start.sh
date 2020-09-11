#!/usr/bin/env bash

# Configuration for Flask app on Heroku environment
FLASK_APP=./app.py 

DB_USERNAME="user0"
DB_PASSWORD="5gdGDHiTfYz0fKD2"
DB_NAME="crescorex"
DATABASE_URI="mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@cluster0-nzzqi.mongodb.net/${DB_NAME}?retryWrites=true&w=majority"

export FLASK_APP
export DATABASE_URI
export DB_NAME
export DEBUG="True"
#export FLASK_ENV=production
export FLASK_ENV=development


# Configuration for `flask_jwt_extended` 
export JWT_SECRET_KEY="anonymity"
export JWT_BLACKLIST_ENABLED="True"

# Start Flask app

pip install -r requirements
pip freeze > requirements.txt
python3 app.py
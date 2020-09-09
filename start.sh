#!/usr/bin/env bash

# Script to start Flask app on Heroku environment
FLASK_APP=./app.py 

DB_USERNAME="user0"
DB_PASSWORD="5gdGDHiTfYz0fKD2"
DB_NAME="crescorex"

DATABASE_URI="mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@cluster0-nzzqi.mongodb.net/${DB_NAME}?retryWrites=true&w=majority"

export FLASK_APP
export DATABASE_URI
export DB_NAME
export DEBUG='True'
export JWT_SECRET_KEY="anonymity"
#export FLASK_ENV=production
export FLASK_ENV=development

flask run
""" Entry point for running this app using GUNICORN """
from app import create_app

heroku_app = create_app()
heroku_app.run()

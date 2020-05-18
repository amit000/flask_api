import os

DEBUG=False
APP_SECRET_KEY = os.environ.get('DATABASE_URI','sqlite:///data.db')
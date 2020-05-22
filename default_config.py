import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
PROPAGATE_EXCEPTIONS = True
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
DEBUG = True
SECRET_KEY = os.environ["APP_SECRET_KEY"]
UPLOADED_IMAGES_DEST = os.path.join("static", "images")  # manage root folder
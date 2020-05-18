from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.item import Item, ItemList
from resources.user import (
    RegisterUser,
    UserResource,
    UserLogin,
    TokenRefresh,
    UserLogout,
)
from ma import ma
from marshmallow import ValidationError
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
load_dotenv(".env",verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": "Session has expired", "error": "stale_token"})


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({"message": "Token is tampered with", "error": "tampered_token"})


@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({"message": "Token is missing", "error": "missing_token"})


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({"message": "Token is not fresh", "error": "not_fresh_token"})


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({"message": "Token has been revoked", "error": "token_revoked"})


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify(err.messages), 400


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(RegisterUser, "/register")
api.add_resource(UserResource, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmationbyuser/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)

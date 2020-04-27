from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.item import Item, ItemList
from resources.user import (
    RegisterUser,
    UserResource,
    UserLogin,
    TokenRefresh,
    UserLogout,
)
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "secretKey"
api = Api(app)
jwt = JWTManager(app)


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


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(RegisterUser, "/register")
api.add_resource(UserResource, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)

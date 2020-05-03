from flask import jsonify, request
from flask_restful import Resource

from blacklist import BLACKLIST
from models.User import User
from schemas.UserSchema import UserSchema
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_claims,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)


FIELD_MISSING_ERROR = "{} can not be left blank"
USER_EXISTS_ERROR = "A user with username '{}' already exists"
USER_CREATED_MSG = "User successfully created"
USER_DELETED_MSG = "User successfully deleted"
USER_NOT_FOUND_MSG = "User does not exist"
INCORRECT_CREDENTIALS_ERROR = "Invalid username or password"
ADMIN_PRIVILEGE_ERROR = "You need admin privileges to delete user"
USER_LOGGED_OUT_MSG = "Successfully Logged Out"

user_schema = UserSchema()


class RegisterUser(Resource):
    def post(self):
        user = user_schema.load(request.get_json())

        if User.find_by_username(user.username):
            return {"message": USER_EXISTS_ERROR.format(user.username)}, 400

        user.create_user()
        return {"message": USER_CREATED_MSG}, 201


class UserResource(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = User.find_by_id(user_id)
        return (
            user_schema.dump(user) if user else ({"message": USER_NOT_FOUND_MSG}, 404)
        )

    @classmethod
    @jwt_required
    def delete(cls, user_id: int):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": ADMIN_PRIVILEGE_ERROR}, 401
        user = User.find_by_id(user_id)
        if user:
            user.delete_user()
            return {"message": USER_DELETED_MSG}, 200
        return {"message": USER_NOT_FOUND_MSG}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json())

        print(user_data)
        user = User.find_by_username(user_data.username)
        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INCORRECT_CREDENTIALS_ERROR}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return jsonify({"message": USER_LOGGED_OUT_MSG})


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": access_token}, 200

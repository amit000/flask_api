from flask import jsonify, request
from flask_restful import Resource

from blacklist import BLACKLIST
from libs.strings import gettext
from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.user import UserSchema
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


user_schema = UserSchema()


class RegisterUser(Resource):
    def post(self):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return (
                {"message": gettext("user_USER_EXISTS_ERROR").format(user.username)},
                400,
            )

        if UserModel.find_by_email(user.email):
            return (
                {"message": gettext("user_EMAIL_EXISTS_ERROR").format(user.email)},
                400,
            )

        user.create_user()
        confirmation = ConfirmationModel(user.id)
        confirmation.save_to_db()
        user.send_confirmation_email()
        return {"message": gettext("user_USER_CREATED_MSG")}, 201


class UserResource(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        return (
            user_schema.dump(user)
            if user
            else ({"message": gettext("user_USER_NOT_FOUND_MSG")}, 404)
        )

    @classmethod
    @jwt_required
    def delete(cls, user_id: int):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": gettext("user_ADMIN_PRIVILEGE_ERROR")}, 401
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_user()
            return {"message": gettext("user_USER_DELETED_MSG")}, 200
        return {"message": gettext("user_USER_NOT_FOUND_MSG")}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(
            request.get_json(), partial=("email", "confirmation",)
        )

        print(user_data)
        user = UserModel.find_by_username(user_data.username)
        if user and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return (
                    {"access_token": access_token, "refresh_token": refresh_token},
                    200,
                )
            return (
                {
                    "message": gettext("user_USER_NOT_ACTIVATED_ERR").format(
                        user.username
                    )
                },
                400,
            )
        return {"message": gettext("user_INCORRECT_CREDENTIALS_ERROR")}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return jsonify({"message": gettext("user_USER_LOGGED_OUT_MSG")})


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": access_token}, 200

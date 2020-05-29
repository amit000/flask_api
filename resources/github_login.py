from flask import request, g, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource

from models.user import UserModel
from oa import github
from schemas.user import UserSchema

user_schema = UserSchema()


class GitHubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(
            callback="http://localhost:5000/login/github/authorized"
        )


class GitHubAuth(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()
        if resp is None or resp.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"],
            }
            return error_response
        g.access_token = resp["access_token"]
        github_user = github.get("user")
        github_username = github_user.data["login"]

        user = UserModel.find_by_username(github_username)
        if not user:
            user = user_schema.load(
                {
                    "username": github_username,
                    "password": "temppassword",
                    "email": "tempemail@temp.com",
                }
            )
            user.create_user()
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}

from flask_restful import Resource, reqparse
from models.User import User
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_claims,
                                jwt_refresh_token_required,
                                get_jwt_identity)

_parser = reqparse.RequestParser()
_parser.add_argument('username',
                     type=str,
                     required=True,
                     help='this field can not be left blank'
                     )
_parser.add_argument('password',
                     type=str,
                     required=True,
                     help='this field can not be left blank'
                     )


class RegisterUser(Resource):

    def post(self):
        data = _parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exits'}, 400

        user = User(**data)
        user.create_user()
        return {'message': 'user created successfully'}, 201


class UserResource(Resource):
    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        return user.json() if user else ({"message": "user does not exist"}, 404)

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'You need admin privileges to delete user'}, 401
        user = User.find_by_id(user_id)
        if user:
            user.delete_user()
            return {"message": "user successfully deleted"}, 200
        return {"message": "user not found"}, 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _parser.parse_args()
        user = User.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': "invalid username or password"}, 401


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': access_token}, 200

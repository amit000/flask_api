import sqlite3
from flask_restful import Resource, reqparse
from models.User import User


class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='this field can not be left blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='this field can not be left blank'
                        )

    def post(self):
        data = RegisterUser.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exits'}, 400

        user = User(**data)
        user.create_user()
        return {'message': 'user created successfully'}, 201

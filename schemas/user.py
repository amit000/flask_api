from marshmallow import post_load, pre_dump

from ma import ma
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    confirmation = ma.Nested(ConfirmationSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")

    @pre_dump
    def dump_it(self, user: UserModel, **kwargs):
        user.confirmation = [user.most_recent_confirmation]
        # print(user.confirmation[0].id)
        return user

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)

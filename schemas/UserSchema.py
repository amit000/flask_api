from marshmallow import post_load, pre_dump

from ma import ma
from models.User import User
from schemas.confirmation import ConfirmationSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    confirmation = ma.Nested(ConfirmationSchema, many=True)
    class Meta:
        model = User
        load_only = ("password",)
        dump_only = ("id","confirmation")

    @pre_dump
    def dump_it(self, user: User, **kwargs):
        user.confirmation = [user.most_recent_confirmation]
        #print(user.confirmation[0].id)
        return user

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

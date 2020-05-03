from marshmallow import post_load

from ma import ma
from models.User import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ("password",)
        dump_only = ("id",)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

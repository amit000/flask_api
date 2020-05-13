from marshmallow import post_load, pre_dump

from ma import ma
from models.User import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ("password",)
        dump_only = (
            "id",
            "confirmation",
        )

    @pre_dump
    def _pre_dump(self, user: User):
        user.confirmation = [user.most_recent_confirmation]
        return user

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

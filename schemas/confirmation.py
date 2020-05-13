from marshmallow import post_load

from ma import ma
from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ("user",)
        dump_only = ("id", "expired_at", "confirmed")
        include_fk = True

    @post_load
    def make_item(self, data, **kwargs):
        return ConfirmationModel(**data)

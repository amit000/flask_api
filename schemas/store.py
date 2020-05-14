from marshmallow import post_load

from ma import ma
from models.item import ItemModel
from models.store import StoreModel
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        dump_only = ("id",)
        include_fk = True

    @post_load
    def make_store(self, data, **kwargs):
        return StoreModel(**data)

from marshmallow import post_load

from ma import ma
from models.Item import ItemDO
from models.Store import StoreDO
from schemas.itemschema import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreDO
        dump_only = ("id",)
        include_fk = True

    @post_load
    def make_store(self, data, **kwargs):
        return StoreDO(**data)

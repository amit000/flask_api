from marshmallow import post_load

from ma import ma
from models.Item import ItemDO
from models.Store import StoreDO


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemDO
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True

    @post_load
    def make_item(self, data, **kwargs):
        return ItemDO(**data)

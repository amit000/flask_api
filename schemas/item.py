from marshmallow import post_load

from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True

    @post_load
    def make_item(self, data, **kwargs):
        return ItemModel(**data)

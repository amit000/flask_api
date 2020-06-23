from ma import ma
from models.order import OrderModel, ItemsToOrders

class ItemsToOrderSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ItemsToOrders
        load_only = ("order_id","id","orders","item",)
        dump_only = ("item_id", )
        include_fk = True
        include_relationships = True


class OrderSchema(ma.SQLAlchemyAutoSchema):

    items_list = ma.Nested(ItemsToOrderSchema, many=True)

    class Meta:
        model = OrderModel
        load_only = ("token",)
        dump_only = ("id", "status",)
        include_fk = True
        include_relationships = True
        load_instance = True


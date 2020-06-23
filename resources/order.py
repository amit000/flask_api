from collections import Counter

from flask import request
from flask_restful import Resource

from libs.strings import gettext
from models.item import ItemModel
from models.order import OrderModel, ItemsToOrders
from schemas.order import OrderSchema

order_schema = OrderSchema()


class Order(Resource):
    @classmethod
    def get(cls):
        return order_schema.dump(OrderModel.find_all(),many=True),200


    @classmethod
    def post(cls):
        """Receive payment token and list of items in the body. Create an order and request Stripe API to receive the amount"""
        data = request.get_json()
        items_order_list = []
        item_id_quantities = Counter(data["item_ids"])

        for _id, count in item_id_quantities.most_common():
            item = ItemModel.find_item_by_id(_id)
            if not item:
                return {"message": gettext("order_ITEM_NOT_FOUND").format(_id)}, 404
            items_order_list.append(ItemsToOrders(item_id=_id, quantity=count))

        order = OrderModel(items_list=items_order_list, status="pending")
        order.save_to_db()

        order.set_status("failed")
        order.accept_payment(data["token"])
        order.set_status("complete")
        abc =  order_schema.dump(order)
        return abc, 200

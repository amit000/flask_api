from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_restful import Resource, reqparse
from models.Item import ItemDO

FIELD_MISSING_ERROR = "{} can not be left blank"
ITEM_EXISTS_ERROR = "An item with name {} already exists"
ITEM_CREATED_MSG = "Item created"
ITEM_DELETED_MSG = "Item deleted"


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=FIELD_MISSING_ERROR.format("Price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=FIELD_MISSING_ERROR.format("Store ID")
    )

    @fresh_jwt_required
    def get(self, name: str):
        x = ItemDO.find_item_by_name(name)

        return (x.json(), 200) if x else ({"item": None}, 404)

    @jwt_required
    def post(self, name: str):
        if ItemDO.find_item_by_name(name):
            return {"message": ITEM_EXISTS_ERROR.format(name)}, 400

        request_data = Item.parser.parse_args()

        item = ItemDO(name, **request_data)
        item.upsert_item()
        return {"message": ITEM_CREATED_MSG}, 201

    @jwt_required
    def delete(self, name: str):
        x = ItemDO.find_item_by_name(name)
        if x:
            x.delete()
        return {"message": ITEM_DELETED_MSG}

    @jwt_required
    def put(self, name: str):
        data = Item.parser.parse_args()

        item = ItemDO.find_item_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemDO(name, **data)
        item.upsert_item()
        return item.json()


class ItemList(Resource):
    @jwt_required
    def get(self):
        x = [item.json() for item in ItemDO.find_items()]
        return {"items": x}

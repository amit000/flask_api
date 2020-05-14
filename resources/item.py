from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_restful import Resource
from flask import request

from libs.strings import gettext
from models.Item import ItemDO
from schemas.itemschema import ItemSchema

FIELD_MISSING_ERROR = gettext('item_FIELD_MISSING_ERROR')
ITEM_EXISTS_ERROR = gettext('item_ITEM_EXISTS_ERROR')
ITEM_CREATED_MSG = gettext('item_ITEM_CREATED_MSG')
ITEM_DELETED_MSG = gettext('item_ITEM_DELETED_MSG')

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @fresh_jwt_required
    def get(self, name: str):
        item = ItemDO.find_item_by_name(name)

        return (item_schema.dump(item), 200) if item else ({"item": None}, 404)

    @jwt_required
    def post(self, name: str):
        if ItemDO.find_item_by_name(name):
            return {"message": ITEM_EXISTS_ERROR.format(name)}, 400
        item_json = request.get_json()
        item_json["name"] = name

        item = item_schema.load(item_json)
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
        item_json = request.get_json()
        item_json["name"] = name
        item_data = item_schema.load(item_json)

        item = ItemDO.find_item_by_name(name)

        if item:
            item.price = item_data.price
        else:
            item = item_data
        item.upsert_item()
        return item_schema.dump(item)


class ItemList(Resource):
    @jwt_required
    def get(self):

        return {"items": item_list_schema.dump(ItemDO.find_items())}, 200

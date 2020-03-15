from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.Item import ItemDO


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='this field can not be left blank'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every store must have ID'
                        )
    @jwt_required()
    def get(self, name):
        x = ItemDO.find_item_by_name(name)

        return (x.json(), 200) if x else ({'item': None}, 404)

    @jwt_required()
    def post(self, name):
        if ItemDO.find_item_by_name(name):
            return {'message': "An item with name {} already exists".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = ItemDO(name, request_data['price'], request_data['store_id'])
        item.upsert_item()
        return {'message': 'created'}, 201

    @jwt_required()
    def delete(self, name):
        x = ItemDO.find_item_by_name(name)
        if x:
            x.delete()
        return {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemDO.find_item_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemDO(name, data['price'], data['store_id'])
        item.upsert_item()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        x = [y.json() for y in ItemDO.find_items()]
        return {'items': x}

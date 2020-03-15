from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.Store import StoreDO


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Every store must have a name'
                        )


    @jwt_required()
    def get(self, name):
        x = StoreDO.find_store_by_name(name)

        return (x.json(), 200) if x else ({'store': None}, 404)

    @jwt_required()
    def post(self, name):
        if StoreDO.find_store_by_name(name):
            return {'message': "A store with name {} already exists".format(name)}, 400

        #request_data = Store.parser.parse_args()

        store = StoreDO(name)
        store.upsert_store()
        return {'message': 'created'}, 201

    @jwt_required()
    def delete(self, name):
        x = StoreDO.find_store_by_name(name)
        if x:
            x.delete()
        return {'message': 'Store deleted'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        x = [y.json() for y in StoreDO.find_stores()]
        return {'stores': x}

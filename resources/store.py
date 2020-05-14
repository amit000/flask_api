from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request

from libs.strings import gettext
from models.store import StoreModel
from schemas.store import StoreSchema


store_schema = StoreSchema()


class Store(Resource):
    @jwt_required
    def get(self, name: str):
        x = StoreModel.find_store_by_name(name)

        return (store_schema.dump(x), 200) if x else ({"store": None}, 404)

    @jwt_required
    def post(self, name: str):
        if StoreModel.find_store_by_name(name):
            return {"message": gettext("store_STORE_EXISTS_ERROR").format(name)}, 400

        store_json = request.get_json()
        store_json["name"] = name
        store = store_schema.load(store_json)
        store.upsert_store()
        return {"message": (gettext("store_STORE_CREATED_MSG"))}, 201

    @jwt_required
    def delete(self, name: str):
        x = StoreModel.find_store_by_name(name)
        if x:
            x.delete()
        return {"message": (gettext("store_STORE_DELETED_MSG"))}


class StoreList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()

        x = (
            [store_schema.dump(store) for store in StoreModel.find_stores()]
            if user_id
            else [store.noid_json() for store in StoreModel.find_stores()]
        )
        return {"stores": x}

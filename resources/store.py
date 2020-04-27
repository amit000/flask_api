from flask_jwt import jwt_required
from flask_jwt_extended import jwt_optional, get_jwt_identity
from flask_restful import Resource, reqparse
from models.Store import StoreDO

FIELD_MISSING_ERROR = "{} can not be left blank"
STORE_EXISTS_ERROR = "A store with name {} already exists"
STORE_CREATED_MSG = "Store successfully created"
STORE_DELETED_MSG = "Store successfully deleted"


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help=FIELD_MISSING_ERROR.format("Name")
    )

    @jwt_required
    def get(self, name: str):
        x = StoreDO.find_store_by_name(name)

        return (x.json(), 200) if x else ({"store": None}, 404)

    @jwt_required
    def post(self, name: str):
        if StoreDO.find_store_by_name(name):
            return {"message": STORE_EXISTS_ERROR.format(name)}, 400

        store = StoreDO(name)
        store.upsert_store()
        return {"message": STORE_CREATED_MSG}, 201

    @jwt_required
    def delete(self, name: str):
        x = StoreDO.find_store_by_name(name)
        if x:
            x.delete()
        return {"message": STORE_DELETED_MSG}


class StoreList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()

        x = (
            [store.json() for store in StoreDO.find_stores()]
            if user_id
            else [store.noid_json() for store in StoreDO.find_stores()]
        )
        return {"stores": x}

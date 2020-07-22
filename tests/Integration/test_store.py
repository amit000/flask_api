from tests.Integration.base_test import BaseTest

from schemas.item import ItemSchema
from schemas.store import StoreSchema
from models.item import ItemModel
from models.store import StoreModel


class TestStore(BaseTest):
    item_schema = ItemSchema()
    store_schema = StoreSchema()

    def setUp(self):
        BaseTest.setUp(self)

        with self.app_context():
            store = self.store_schema.load({"name": "amazon"})
            store.upsert_store()

            new_item = self.item_schema.load(
                {"name": "test_name", "price": "23.45", "store_id": 1}
            )

            new_item.upsert_item()

    def test_crud(self):
        with self.app_context():
            store = StoreModel.find_store_by_id(1)
            self.assertIsNotNone(store)
            self.assertEqual(store, StoreModel.find_store_by_name("amazon"))
            self.assertEqual(1, store.id)
            self.assertEqual("amazon", store.name)
            self.assertListEqual(
                ["test_name"], [item.name for item in store.items.all()]
            )
            self.assertDictEqual(
                {
                    "id": 1,
                    "items": [
                        {"id": 1, "store_id": 1, "name": "test_name", "price": 23.45}
                    ],
                    "name": "amazon",
                },
                self.store_schema.dump(store),
            )
            store.delete()
            self.assertIsNone(StoreModel.find_store_by_id(1))
            self.assertIsNone(StoreModel.find_store_by_name("amazon"))

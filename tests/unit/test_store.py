from unittest import TestCase

from schemas.store import StoreSchema
from models.store import StoreModel


class TestStore(TestCase):
    store_schema = StoreSchema()

    def test_load_store(self):
        new_store = self.store_schema.load({"name": "amazon"})

        self.assertIsInstance(new_store, StoreModel)
        self.assertEqual(new_store.name, "amazon")

    def test_dump_store(self):
        new_store = self.store_schema.load({"name": "amazon"})
        self.assertDictEqual(
            self.store_schema.dump(new_store),
            {"id": None, "items": [], "name": "amazon"},
        )

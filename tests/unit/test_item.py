from unittest import TestCase

from schemas.item import ItemSchema
from models.item import ItemModel


class TestItem(TestCase):
    item_schema = ItemSchema()

    def test_load_item(self):
        new_item = self.item_schema.load({"name": "test_name", "price": "23.45"})

        self.assertEqual(new_item.name, "test_name")
        self.assertEqual(new_item.price, 23.45)
        self.assertIsInstance(new_item, ItemModel)
        self.assertNotEqual(new_item.price, 23.44)
        self.assertNotEqual(new_item.price, 23.46)

    def test_dump_item(self):
        new_item = self.item_schema.load({"name": "test_name", "price": "23.45"})
        self.assertDictEqual(
            self.item_schema.dump(new_item),
            {"name": "test_name", "price": 23.45, "store_id": None, "id": None},
        )

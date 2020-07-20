from tests.Integration.base_test import BaseTest
from schemas.item import ItemSchema
from models.item import ItemModel


class ItemTest(BaseTest):
    item_schema = ItemSchema()

    def test_crud(self):

        with self.app_context():

            new_item = self.item_schema.load({"name": "test_name", "price": "23.45"})

            self.assertIsNone(ItemModel.find_item_by_name("test_name"))
            new_item.upsert_item()

            self.assertIsInstance(ItemModel.find_item_by_name("test_name"), ItemModel)

            self.assertEqual(
                ItemModel.find_item_by_id(1), ItemModel.find_item_by_name("test_name")
            )
            new_item1 = self.item_schema.load({"name": "test_name1", "price": "23.45"})
            new_item1.upsert_item()

            self.assertListEqual(ItemModel.find_items(), [new_item, new_item1])

            new_item.delete()
            self.assertIsNone(ItemModel.find_item_by_name("test_name"))

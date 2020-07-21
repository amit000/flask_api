from tests.Integration.base_test import BaseTest

from schemas.order import ItemsToOrderSchema
from schemas.order import OrderSchema
from schemas.item import ItemSchema
from models.item import ItemModel
from models.order import OrderModel
from models.order import ItemsToOrders


class TestOrder(BaseTest):
    items_to_order = ItemsToOrderSchema()
    order_schema = OrderSchema()
    item_schema = ItemSchema()

    def setUp(self):
        BaseTest.setUp(self)
        with self.app_context():
            new_item = self.item_schema.load({"name": "test_name", "price": "22.43"})
            new_item1 = self.item_schema.load({"name": "test_name1", "price": "23.47"})
            new_item1.upsert_item()
            new_item.upsert_item()
            order = OrderModel(
                items_list=[
                    ItemsToOrders(item_id=1, quantity=3),
                    ItemsToOrders(item_id=2, quantity=2),
                ],
                status="pending",
            )
            order.save_to_db()

    def test_order(self):
        with self.app_context():
            print(self.order_schema.dump(OrderModel.find_all(), many=True))

    def test_set_status(self):
        with self.app_context():
            order1 = OrderModel.find_by_id(1)
            order1.set_status("failed")
            self.assertEqual("failed", order1.status)

    def test_amount(self):
        with self.app_context():
            order1 = OrderModel.find_by_id(1)
            self.assertEqual(11527, order1.amount)

    def test_description(self):
        with self.app_context():
            order1 = OrderModel.find_by_id(1)
            self.assertListEqual(
                ["3 x test_name1", "2 x test_name"], order1.description
            )

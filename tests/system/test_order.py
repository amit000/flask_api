from unittest import TestCase
from app import app


class Order(TestCase):
    def test_get_all(self):
        with app.test_client() as c:
            resp = c.get("/order")
            print(resp)

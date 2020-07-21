from typing import List

from db import db


class ItemsToOrders(db.Model):
    __tablename__ = "items_to_orders"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("ItemModel")
    orders = db.relationship("OrderModel", back_populates="items_list")


class OrderModel(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    items_list = db.relationship("ItemsToOrders", back_populates="orders")

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.save_to_db()

    @property
    def amount(self) -> int:
        return int(sum([(i.item.price * 100) * i.quantity for i in self.items_list]))

    @property
    def description(self):
        item_counts = [f"{i.quantity} x {i.item.name}" for i in self.items_list]
        return item_counts

    def accept_payment(self, token: str):
        amount = self.amount
        description = self.description
        source = token
        ##TODO call payment method with amount description and token
        # print(amount,description)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

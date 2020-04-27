from typing import Dict, List, Union
from db import db

ItemJSON = Dict[str, Union[int, str, float]]


class ItemDO(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreDO")

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJSON:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    @classmethod
    def find_item_by_name(cls, name: str) -> "ItemDO":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_items(cls) -> List["ItemDO"]:
        return cls.query.all()

    @classmethod
    def find_item_by_id(cls, _id: int) -> "ItemDO":
        return cls.query.filter_by(id=_id).first()

    def upsert_item(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

from typing import List
from db import db


class ItemDO(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreDO")

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

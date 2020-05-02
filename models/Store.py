from typing import Dict, List, Union

from models.Item import ItemJSON
from db import db

StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]


class StoreDO(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship("ItemDO", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self) -> StoreJSON:
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }

    def noid_json(self) -> Dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def find_store_by_name(cls, name: str) -> "StoreDO":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_stores(cls) -> List["StoreDO"]:
        return cls.query.all()

    @classmethod
    def find_store_by_id(cls, _id: int) -> "StoreDO":
        return cls.query.filter_by(id=_id).first()

    def upsert_store(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

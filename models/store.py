from typing import Dict, List

from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    items = db.relationship("ItemModel", lazy="dynamic")

    def noid_json(self) -> Dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def find_store_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_stores(cls) -> List["StoreModel"]:
        return cls.query.all()

    @classmethod
    def find_store_by_id(cls, _id: int) -> "StoreModel":
        return cls.query.filter_by(id=_id).first()

    def upsert_store(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

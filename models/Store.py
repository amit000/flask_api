from db import db


class StoreDO(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemDO', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [y.json() for y in self.items.all()]}

    @classmethod
    def find_store_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_stores(cls):
        return cls.query.all()

    @classmethod
    def find_store_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def upsert_store(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

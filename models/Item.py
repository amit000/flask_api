from db import db


class ItemDO(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer,db.ForeignKey('stores.id'))
    store = db.relationship('StoreDO')


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
                'id': self.id,
                'name': self.name,
                'price': self.price,
                'store_id': self.store_id
                }

    @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_items(cls):
        return cls.query.all()

    @classmethod
    def find_item_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def upsert_item(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

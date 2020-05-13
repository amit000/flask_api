import os
from time import time
from uuid import uuid4

from db import db


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + int(
            os.environ.get("CONFIRMATION_EXPIRATION_DELTA")
        )
        self.confirmed = False

    @classmethod
    def find_by_id(cls, id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=id).first()

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def forced_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = time()
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.remove(self)
        db.session.commit()

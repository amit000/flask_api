from flask import request, url_for

from libs.mailgun import send_conf_email
from libs.strings import gettext
from models.confirmation import ConfirmationModel
from db import db

SUBJECT = gettext("user_email_SUBJECT")
TEXT = gettext("user_email_TEXT")
HTML = gettext("user_email_HTML")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def most_recent_confirmation(self) -> ConfirmationModel:
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @classmethod
    def find_by_username(cls, username: str) -> "User":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "User":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        return cls.query.filter_by(email=email).first()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation.id
        )
        send_conf_email(
            self.email,
            SUBJECT.format(self.username),
            TEXT.format(self.username, link),
            HTML.format(self.username, link, link),
        )

    def create_user(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_user(self) -> None:
        db.session.delete(self)
        db.session.commit()

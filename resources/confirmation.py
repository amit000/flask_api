from time import time

from flask import make_response, render_template
from flask_restful import Resource

from libs.strings import gettext
from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.confirmation import ConfirmationSchema


confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """Return confirmation HTML page"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": (gettext("confirmation_NOT_FOUND"))}, 404
        if confirmation.expired:
            return {"message": (gettext("confirmation_EXPIRED"))}, 400
        if confirmation.confirmed:
            return {"message": (gettext("confirmation_ALREADY_CONFIRMED"))}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()
        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers,
        )


class ConfirmationByUser(Resource):
    @classmethod
    def post(cls, user_id: int):
        """Resend the confirmation email"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": (gettext("confirmation_NOT_FOUND"))}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                return {"message": (gettext("confirmation_ALREADY_CONFIRMED"))}, 400
            confirmation.forced_to_expire()
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": (gettext("confirmation_RESEND_SCCESSFUL"))}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    @classmethod
    def get(cls, user_id: int):
        """Activate user manually. Use for testing"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": (gettext("confirmation_NOT_FOUND"))}, 404
        return (
            {
                "current time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )

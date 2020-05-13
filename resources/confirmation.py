from time import time

from flask import make_response, render_template
from flask_restful import Resource

from models.User import User
from models.confirmation import ConfirmationModel
from schemas.confirmation import ConfirmationSchema

NOT_FOUND = "User Not Found"
EXPIRED = "Confirmation email expired"
ALREADY_CONFIRMED = "User is already confirmed"
RESEND_SCCESSFUL = "Activation email resend"

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str) -> None:
        """Return confirmation HTML page"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": NOT_FOUND}, 404
        if confirmation.expired:
            return {"message": EXPIRED}, 400
        if confirmation.confirmed:
            return {"message": ALREADY_CONFIRMED}, 400

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
        user = User.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                return {"message": ALREADY_CONFIRMED}, 400
            confirmation.forced_to_expire()
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": RESEND_SCCESSFUL}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    @classmethod
    def get(cls, user_id: int):
        """Activate user manually. Use for testing"""
        user = User.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND}, 404
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

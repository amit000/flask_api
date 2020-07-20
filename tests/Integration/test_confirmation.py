from unittest import TestCase

from schemas.confirmation import ConfirmationSchema
from models.confirmation import ConfirmationModel
from models.user import UserModel


class ConfirmationTest(TestCase):

    confirmation_schema = ConfirmationSchema()

    def test_load_confirmation(self):
        confirmation_model = self.confirmation_schema.load({"user": "2"})

        self.assertIsInstance(confirmation_model, ConfirmationModel)

from unittest import TestCase

from models.user import UserModel
from schemas.user import UserSchema


class UserTest(TestCase):
    user_schema = UserSchema()

    def test_user_load(self):

        abc = self.user_schema.load(
            {"password": "abc", "username": "abc", "email": "abc@asd.com"}
        )

        self.assertEqual(abc.username, "abc")
        self.assertEqual(abc.password, "abc")
        self.assertEqual(abc.email, "abc@asd.com")
        self.assertIsInstance(abc, UserModel)

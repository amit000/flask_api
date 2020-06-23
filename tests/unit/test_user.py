from unittest import TestCase
from schemas.user import UserSchema


class User(TestCase):
    def test_user(self):
        user_name = "test"
        password = "abc123"
        email = "test@test.com"

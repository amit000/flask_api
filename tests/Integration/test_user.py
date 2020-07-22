import time

from tests.Integration.base_test import BaseTest

from schemas.user import UserSchema
from schemas.confirmation import ConfirmationSchema
from models.user import UserModel
from models.confirmation import ConfirmationModel


class TestUser(BaseTest):
    user_schema = UserSchema()
    confirmation_schema = ConfirmationSchema()

    def setUp(self):
        BaseTest.setUp(self)
        with self.app_context():
            user = self.user_schema.load(
                {
                    "username": "testuser",
                    "password": "testpassword",
                    "email": "abc@avc.com",
                }
            )
            user.create_user()

            conf = ConfirmationModel(user.id)
            conf.save_to_db()

    def test_user_confirmation(self):
        with self.app_context():
            user = UserModel.find_by_id(1)
            user.confirmation.first().confirmed = True
            self.assertEqual(user.most_recent_confirmation, user.confirmation.first())

            user1 = UserModel.find_by_username("testuser")

            self.assertEqual(user, user1)

            user2 = UserModel.find_by_id(1)

            self.assertEqual(user, user2)

            user3 = UserModel.find_by_email("abc@avc.com")

            self.assertEqual(user, user3)

    def test_user_conf_expired(self):
        with self.app_context():
            user = UserModel.find_by_id(1)
            conf = user.confirmation.first()
            self.assertIsInstance(conf, ConfirmationModel)

            self.assertEqual(False, conf.expired)

            conf.forced_to_expire()

            time.sleep(0.5)

            self.assertEqual(True, user.confirmation.first().expired)

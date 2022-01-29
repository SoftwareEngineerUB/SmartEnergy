from unittest import TestCase

from app.user.user import UserObject


class Test(TestCase):
    def test_get_mock_user(self):
        user = UserObject.getMockUser()

        self.assertTrue(user)

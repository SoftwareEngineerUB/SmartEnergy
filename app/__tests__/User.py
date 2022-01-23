from unittest import TestCase

from app.meter.route import getMockUser


class Test(TestCase):
    def test_get_mock_user(self):
        user = getMockUser()

        self.assertTrue(user)

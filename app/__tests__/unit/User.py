from unittest import TestCase

from app.user.user import UserObject


def test_get_mock_user():
    user = UserObject.getMockUser()

    assert (bool(user))

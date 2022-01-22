from unittest import TestCase

from app.meter.route import getMockUser, getDevices


class Test(TestCase):
    def test_get_mock_user(self):
        user = getMockUser()

        print(user)

        self.assertTrue(user)

    def test_get_devices(self):
        devices = getDevices()

        print(devices)

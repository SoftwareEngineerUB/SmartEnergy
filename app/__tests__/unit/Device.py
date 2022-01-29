from app.device.device import DeviceObject
from app.user.user import UserObject


def test_create():
    device = DeviceObject.create(UserObject.getMockUser(), {
        "alias": "test"
    })

    # expect that db is modified

    assert(bool(device))


def test_update():
    device = None  # create one

    # update it

    # expect update was successfully (database + return

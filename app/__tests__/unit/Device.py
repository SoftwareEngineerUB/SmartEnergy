from app.device.device import DeviceObject
from app.models import Device
from app.user.user import UserObject


def test_create():
    device = DeviceObject.create(UserObject.getMockUser(), {
        'alias': 'test'
    })

    assert (bool(DeviceObject.find(device.id)))
    assert (bool(device))


def test_update():
    device_alias = 'test'
    device = DeviceObject.create(UserObject.getMockUser(), {
        'alias': device_alias
    })

    assert (bool(device))
    assert (device.alias == device_alias)

    device = DeviceObject(UserObject.getMockUser(), device.id)
    new_alias = 'updated alias'
    new_description = 'this is an updated device'
    device.update({
        'id': device.device_id,
        'alias': new_alias,
        'description': new_description,
    })
    updated_device: Device = DeviceObject.find(device.device_id)

    assert (updated_device.alias == new_alias)
    assert (updated_device.description == new_description)


def test_delete():
    device_alias = 'test'
    device = DeviceObject.create(UserObject.getMockUser(), {
        'alias': device_alias
    })

    assert (bool(DeviceObject.find(device.id)))
    device = DeviceObject(UserObject.getMockUser(), device.id)
    device.delete()
    assert (DeviceObject.find(device.device_id) is None)

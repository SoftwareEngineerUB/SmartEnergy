from app.models import Device

from datetime import datetime


def test_get_devices(client):
    devices = client.get("/devices")

    assert (bool(devices))


def test_add_device(client):
    device_data = dict(
        alias="this is a test device"
    )

    devices = client.get("/devices").json

    number_of_devices_before_add = len(devices)

    device: Device = client.post("/device",
                                 json=device_data).json

    assert (bool(device))

    assert (device['alias'] == device_data['alias'])
    assert (bool(device['uuid']))

    devices = client.get("/devices").json

    assert (len(devices) == number_of_devices_before_add + 1)


def test_get_device(client):
    device_data = dict(
        alias="this is a test device"
    )

    inserted_device: Device = client.post("/device",
                                          json=device_data).json

    device = client.get(
        "/device", query_string=dict(id=inserted_device['id'])).json

    assert (bool(device))

    assert (device['alias'] == device_data['alias'])


def test_add_device_data(client):
    device_data = dict(
        alias="this is a test device"
    )

    device_insert_data = dict(
        time=datetime.now().strftime("%A"),
        value=420
    )

    inserted_device: Device = client.post("/device",
                                          json=device_data).json

    device_insert_data["id"] = inserted_device["id"]

    _ = client.post("/device/data",
                    json=device_insert_data).json

    device_data_response = client.get("/device/data", query_string=dict(
        id=inserted_device["id"],
        page=0,
        per_page=50
    ))

    assert (bool(device_data_response))


def test_get_is_device_left_running(client):
    device_data = dict(
        alias="this is a test device"
    )

    device: Device = client.post("/device",
                                 json=device_data).json

    response = client.get("/device/left_running",
                          query_string=dict(
                              id=device['id']
                          ))

    print(response)

    # TODO: expect it to not be running, and then turn it on / off & test


def test_get_device_consumption(client):
    device_data = dict(
        alias="this is a test device"
    )

    device: Device = client.post("/device",
                                 json=device_data).json

    response = client.get("/device/predict_consumption",
                          query_string=dict(
                              id=device['id']
                          )).json

    print(response)
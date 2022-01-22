import json

from flask import Blueprint, jsonify, request

from app.meter.device import DeviceObject
from app.meter.meter import Meter
from app.models import User
from app.models.db import db
from app.mqtt.mqtt_hub import MqttHub

app_meter = Blueprint('app_contents', __name__)


def getMockUser():
    username = 'mock-user'
    return db.session.query(User).filter_by(username=username).first()


@app_meter.route('/devices', methods=['GET'])
def getDevices():
    meter = Meter(getMockUser())

    return jsonify([x.json() for x in meter.devices])


@app_meter.route('/device', methods=['GET'])
def getDevice():
    device_id = int(request.args.get("id", None))

    device = DeviceObject(getMockUser(), device_id)

    return jsonify(device.device.json())


@app_meter.route('/device', methods=['POST'])
def addDevice():
    device_json = json.loads(request.body)
    device = DeviceObject.create(getMockUser(), device_json)

    return jsonify(device.json())


@app_meter.route('/device/data', methods=['POST'])
def addDeviceData():
    data = json.loads(request.body)

    device_id = int(data["id"])
    time = data["time"]
    value = float(data["time"])

    device = DeviceObject(getMockUser(), device_id)
    device.addData(time, value)

    return jsonify(device.device.json())


@app_meter.route('/device/data', methods=['GET'])
def getDeviceData():
    device_id = int(request.args.get("id", None))
    page = int(request.args.get("page", 0))
    per_page = int(request.args.get("per_page", 100))

    device = DeviceObject(getMockUser(), device_id)
    data = device.getData(device_id, page, per_page)

    return jsonify(data)


@app_meter.route('/devices/start', methods=['GET'])
def startDevices():
    # does not actually start the devices
    # but executes initialization functions for the scheduler
    # and enforces device settings

    MqttHub.handle.initialize_scheduler()

    # TODO status code or smth
    return "started"
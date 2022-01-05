from datetime import datetime

from flask import Blueprint, jsonify, request

from app.meter.device import DeviceObject
from app.meter.meter import Meter
from app.models import User
from app.models.db import db

app_meter = Blueprint('app_contents', __name__)


def getMockUser():
    username = 'mock-user'
    return db.session.query(User).filter_by(username=username).first()


@app_meter.route('/api/get/devices', methods=['GET'])
def getDevices():
    meter = Meter(getMockUser())

    return jsonify([x.json() for x in meter.devices])


@app_meter.route('/api/get/device', methods=['GET'])
def getDevice():
    device_id = int(request.args.get("id", None))

    device = DeviceObject(getMockUser(), device_id)

    return jsonify(device.device.json())


@app_meter.route('/api/post/device/data', methods=['GET'])
def addDeviceData():
    device_id = int(request.args.get("id", None))
    time = request.args.get("time", str(datetime.now()))
    value = float(request.args.get("value", 0))

    device = DeviceObject(getMockUser(), device_id)
    device.addData(time, value)

    return jsonify(device.device.json())

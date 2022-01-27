import json

from flask import Blueprint, jsonify, request

from app.meter.device import DeviceObject
from app.meter.meter import Meter
from app.models import User
from app.models.db import db
from app.mqtt.mqtt_hub import MqttHub
from app.util.ML.data_manipulator import setDataForTrain

app_meter = Blueprint('app_contents', __name__)


def getMockUser() -> User:
    username = 'mock-user'
    return db.session.query(User).filter_by(username=username).first()


@app_meter.route("/internal/generate_train_data", methods=['GET'])
def generate_train_data():
    meter = Meter(getMockUser())
    for device in meter.devices:
        deviceObj = DeviceObject(getMockUser(), device.id)
        setDataForTrain(deviceObj)

        print(f"Device with id={device.id} done")
    return "Done"


@app_meter.route("/device_left_running", methods=['GET'])
def getIsDeviceLeftRunning():
    device_id = int(request.args.get("id", 0))
    if device_id == 0:
        return jsonify("Bad argument")

    device = DeviceObject(getMockUser(), device_id)
    return str(device.isDeviceLeftRunning())


@app_meter.route('/predict_consumption', methods=['GET'])
def getDeviceConsumption():
    mock_start_time = '2015-01-01 00:30:00'
    mock_end_time = '2015-01-01 06:30:00'
    # TODO: handle endpoint cases
    device_id = int(request.args.get("id", 0))
    if device_id == 0:
        return jsonify("Bad argument")

    device = DeviceObject(getMockUser(), device_id)
    return str(device.predictConsumption(mock_start_time, mock_end_time))
    

@app_meter.route('/anomaly/check', methods=['GET'])
def mockAnomalyCheck():
    device = DeviceObject(getMockUser(), 1)
    timestamp = '2015-01-01 00:30:00'

    return jsonify(device.anomalyCheck(timestamp))
  
@app_meter.route('/devices', methods=['GET'])
def getDevices() -> json:
    meter = Meter(getMockUser())

    return jsonify([x.json() for x in meter.devices])


@app_meter.route('/device', methods=['GET'])
def getDevice():
    device_id = int(request.args.get("id", 0))

    device = DeviceObject(getMockUser(), device_id)

    return jsonify(device.device.json())


@app_meter.route('/device', methods=['POST'])
def addDevice():
    device_json = json.loads(request.json)

    device = DeviceObject.create(getMockUser(), device_json)

    return jsonify(device.json())


@app_meter.route('/device/data', methods=['POST'])
def addDeviceData():
    data = json.loads(request.json)

    device_id = int(data["id"])
    time = data["time"]
    value = float(data["value"])

    device = DeviceObject(getMockUser(), device_id)
    device.addData(time, value)

    return jsonify(device.device.json())


@app_meter.route('/device/data', methods=['GET'])
def getDeviceData():
    device_id = int(request.args.get("id", 0))
    page = int(request.args.get("page", 0))
    per_page = int(request.args.get("per_page", 100))

    device = DeviceObject(getMockUser(), device_id)

    data = device.getData(page, per_page)

    return jsonify(data)


@app_meter.route('/devices/start', methods=['GET'])
def startDevices():
    # does not actually start the devices
    # but executes initialization functions for the scheduler
    # and enforces device settings

    MqttHub.handle.initialize_scheduler()

    # TODO status code or smth
    return "started"

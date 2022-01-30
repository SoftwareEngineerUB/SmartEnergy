from datetime import datetime
import json

from flask import Blueprint, jsonify, request
from flask import Response

from app.device.device import DeviceObject
from app.device.meter import Meter
from app.user.user import UserObject
from app.util.ML.data_manipulator import setDataForTrain


app_device = Blueprint('device', __name__)


@app_device.route("/device/internal/generate_train_data", methods=['GET'])
def generate_train_data():
    key = int(request.args.get("key", 0))
    if key != 1234:
        return Response("Unauthorized", status=403)

    meter = Meter(UserObject.getMockUser())
    for device in meter.devices:
        deviceObj = DeviceObject(UserObject.getMockUser(), device.id)
        setDataForTrain(deviceObj)

        print(f"Device with id={device.id} done")
    return Response("Done", status=200)


# Statistics for Devices
@app_device.route("/device/predict_left_running", methods=['GET'])
def predictIsDeviceLeftRunning():
    device_id = int(request.args.get("id", -1))
    if device_id == -1:
        return Response(jsonify("Bad argument"), status=400)

    device = DeviceObject(UserObject.getMockUser(), device_id)
    return jsonify(device.predictDeviceLeftRunning())


@app_device.route('/device/predict_consumption', methods=['GET'])
def getDeviceConsumption():
    start_time = request.args.get("start-time", '2015-01-01 00:30:00')
    end_time = request.args.get("start-time", '2015-01-01 06:30:00')
    device_id = int(request.args.get("id", -1))

    if device_id == -1:
        return Response(jsonify("Bad argument"), status=400)

    device = DeviceObject(UserObject.getMockUser(), device_id)

    return jsonify(str(device.predictConsumption(start_time, end_time)))


@app_device.route('/device/anomaly_check', methods=['GET'])
def getAnomalyCheck():
    
    device = DeviceObject(UserObject.getMockUser(), 1)
    timestamp = request.args.get("timestamp", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    return jsonify(device.anomalyCheck(timestamp))


# CRUD API Devices
@app_device.route('/devices', methods=['GET'])
def getDevices() -> json:
    meter = Meter(UserObject.getMockUser())

    return jsonify([x.json() for x in meter.devices])


@app_device.route('/device', methods=['GET'])
def getDevice():
    device_id = int(request.args.get("id", 0))

    device = DeviceObject(UserObject.getMockUser(), device_id)

    return jsonify(device.device.json())


@app_device.route('/device', methods=['POST'])
def addDevice():
    device_json = request.json

    device = DeviceObject.create(UserObject.getMockUser(), device_json)

    return jsonify(device.json())


@app_device.route('/device', methods=['PUT'])
def updateDevice():
    device_json = request.json

    device = DeviceObject(UserObject.getMockUser(), device_json['id'])
    device.update({
        'alias': device_json['alias'],
        'description': device_json['description'],
    })

    return jsonify(device.device.json())


@app_device.route('/device', methods=['DELETE'])
def deleteDevice():
    request_data = request.json

    device = DeviceObject(UserObject.getMockUser(), request_data['id'])
    device.delete()

    return jsonify(True)


@app_device.route('/device/data', methods=['POST'])
def addDeviceData():
    data = request.json

    device_id = int(data["id"])
    time = data["time"]
    value = float(data["value"])

    device = DeviceObject(UserObject.getMockUser(), device_id)

    device.addData(time, value)

    return jsonify(device.device.json())


@app_device.route('/device/data', methods=['GET'])
def getDeviceData():
    device_id = int(request.args.get("id", 0))
    page = int(request.args.get("page", 0))
    per_page = int(request.args.get("per_page", 100))

    device = DeviceObject(UserObject.getMockUser(), device_id)

    data = device.getData(page, per_page)

    return jsonify(data)

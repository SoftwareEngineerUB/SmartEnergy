from datetime import date, datetime
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
    """
    Generates the data for training the ML model
    ----
    """
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
    """
    Returns if the device is presumed left running without a real need
    ----

     parameters:
      - name: device_id
        in: query
        description: the device id for which the prediction is made
        required: false
        style: form
        explode: true
        schema:
          type: integer
          format: int32
      responses:
        "200":
          description: A boolean, True or False, if the device is left running or not
          content:
            application/json:
              schema:
                type: boolean
        "400":
          description: Bad argument
    """
    device_id = int(request.args.get("id", -1))
    if device_id == -1:
        return Response(jsonify("Bad argument"), status=400)

    device = DeviceObject(UserObject.getMockUser(), device_id)
    return jsonify(device.predictDeviceLeftRunning())


@app_device.route('/device/predict_consumption', methods=['GET'])
def getDeviceConsumptionPrediction():
    """
    Returns the predicted consumption for a device in a given timeframe
    ----

    parameters:
      - name: start_time
        in: query
        description: the start date of the given timeframe
        required: false
        style: form
        explode: true
        schema:
          type: string
          format: YYYY-MM-DD HH:MM:SS
      - name: end_time
        in: query
        description: the end date of the given timeframe
        required: false
        style: form
        explode: true
        schema:
          type: string
          format: YYYY-MM-DD HH:MM:SS
      - name: device_id
        in: query
        description: the device id for which the prediction is made
        required: false
        style: form
        explode: true
        schema:
          type: integer
          format: int32
      responses:
        "200":
          description: The predicted consumption, in kW
          content:
            application/json:
              schema:
                type: integer
        "400":
          description: Bad argument
    """
    start_time = request.args.get("start-time", '2015-01-01 00:30:00')
    end_time = request.args.get("start-time", '2015-01-01 06:30:00')
    device_id = int(request.args.get("id", -1))

    if device_id == -1:
        return Response(jsonify("Bad argument"), status=400)

    device = DeviceObject(UserObject.getMockUser(), device_id)

    return jsonify(str(device.predictConsumption(start_time, end_time)))


@app_device.route('/device/anomaly_check', methods=['GET'])
def getAnomalyCheck():
    """
    Returns True if the consumption profile of a given device in an interval of 6 hours is annormal
    ----

    parameters:
      - name: timestamp
        in: query
        description: the start date of the 6 hour period for which the consumption is tested
        required: false
        style: form
        explode: true
        schema:
          type: string
          format: YYYY-MM-DD HH:MM:SS
      - name: device_id
        in: query
        description: the device id for which the prediction is made
        required: false
        style: form
        explode: true
        schema:
          type: integer
          format: int32
      responses:
        "200":
          description: True, if the consumption is very different from the predicted consumption, False otherwise
          content:
            application/json:
              schema:
                type: boolean
        "403":
          description: Invalid parameters
    """
    try:
        device_id = int(request.args.get("device_id", -1))
        timestamp = request.args.get("timestamp", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    except:
        return Response("Invalid parameters", status=403)
    if device_id == -1:
        return Response("Invalid parameters", status=403)

    device = DeviceObject(UserObject.getMockUser(), device_id)
    return jsonify(device.anomalyCheck(timestamp))


# CRUD API Devices
@app_device.route('/devices', methods=['GET'])
def getDevices() -> json:
    """
    Returns all devices registered in database
    ---
    
    responses:
        "200":
          description: All devices from database
    """
    meter = Meter(UserObject.getMockUser())

    return jsonify([x.json() for x in meter.devices])


@app_device.route('/device', methods=['GET'])
def getDevice():
    """
    Return a specific device
    ----

    parameters:
      - name: id
        in: query
        description: Device id
        required: false
        style: form
        explode: true
        schema:
          type: number
          format: int32
    responses:
        "200":
          description: Device details
          content:
            application/json:
    """
    device_id = int(request.args.get("id", 0))

    device = DeviceObject(UserObject.getMockUser(), device_id)

    return jsonify(device.device.json())


@app_device.route('/device', methods=['POST'])
def addDevice():
    """
    Add device to database
    ---

    parameters:
      - name: device
        in: header
        description: Device
        required: false
        style: simple
        explode: false
        schema:
          $ref: '#/components/schemas/Device'
      responses:
        "200":
          description: Newly added device
          content:
            application/json:
    """
    device_json = request.json

    device = DeviceObject.create(UserObject.getMockUser(), device_json)

    return jsonify(device.json())


@app_device.route('/device', methods=['PUT'])
def updateDevice():
    """
    Update device
    ---

    parameters:
      - name: device
        in: header
        description: Device
        required: false
        style: simple
        explode: false
        schema:
          $ref: '#/components/schemas/Device'
    responses:
        "200":
          description: Newly updated device
          content:
            application/json:
    """
    device_json = request.json

    device = DeviceObject(UserObject.getMockUser(), device_json['id'])
    device.update({
        'alias': device_json['alias'],
        'description': device_json['description'],
    })

    return jsonify(device.device.json())


@app_device.route('/device', methods=['DELETE'])
def deleteDevice():
    """
    Delete device from database
    ----

    parameters:
      - name: id
        in: query
        description: Device id
        required: false
        style: form
        explode: true
        schema:
          type: number
          format: int32
    responses:
        "200":
          description: True or False if the device has been deleted successfully
          content:
            application/json:
    """
    request_data = request.json

    device = DeviceObject(UserObject.getMockUser(), request_data['id'])
    response = device.delete()

    return jsonify(response)


@app_device.route('/device/data', methods=['POST'])
def addDeviceData():
    """
    Insert device data in database
    ----

    parameters:
      - name: id
        in: header
        description: Device id
        required: false
        style: simple
        explode: false
        schema:
          type: number
          format: int32
      - name: time
        in: header
        description: Time and Date
        required: false
        style: simple
        explode: false
        schema:
          type: string
          format: YYYY-MM-DD HH:MM:SS
      - name: value
        in: header
        description: Consumption value
        required: false
        style: simple
        explode: false
        schema:
          type: number
          format: int32
      responses:
        "200":
          description: True or False if the device data has been inserted successfully
          content:
            application/json:
    """
    data = request.json

    device_id = int(data["id"])
    time = data["time"]
    value = float(data["value"])

    device = DeviceObject(UserObject.getMockUser(), device_id)

    response = device.addData(time, value)

    return jsonify(response)


@app_device.route('/device/data', methods=['GET'])
def getDeviceData():
    """
    Get device data
    ----

    parameters:
      - name: id
        in: query
        description: Device id
        required: false
        style: form
        explode: true
        schema:
          type: number
          format: int32
      - name: page
        in: query
        description: Page id
        required: false
        style: form
        explode: true
        schema:
          type: number
          format: int32
      - name: per_page
        in: query
        description: Items per page
        required: false
        style: form
        explode: true
        schema:
          type: number
          format: int32
      responses:
        "200":
          description: Device details
          content:
            application/json:
    """
    device_id = int(request.args.get("id", 0))
    page = int(request.args.get("page", 0))
    per_page = int(request.args.get("per_page", 100))

    device = DeviceObject(UserObject.getMockUser(), device_id)

    data = device.getData(page, per_page)

    return jsonify(data)

import random
import uuid
from typing import Optional
from sqlalchemy import text

import dateutil.parser

from app.models import User, Device, Data
from app.models.db import db
from app.util.ML.anomaly_detector import AnomalyDetector


class DeviceObject:
    def __init__(self, user: User, device_id: int):
        self.device: Optional[Device] = None
        self.user: User = user
        self.device_id: int = device_id
        self.load()

    @staticmethod
    def create(user: User, device_json) -> Device:
        device = Device(
            alias=device_json['name'],
            uuid=str(uuid.uuid4()),
            description=f"{device_json['name']} mock device",
            status=True,
            settings=dict(),
            user_id=user.id,
        )
        db.session.add(device)

        db.session.flush()
        db.session.refresh(device)

        return device

    def load(self):
        device = db.session.query(Device).filter_by(user_id=self.user.id, id=self.device_id).first()
        self.device = device

    def addData(self, time: str, value: float):
        data = Data(
            time=dateutil.parser.parse(time),
            value=value,
            device_id=self.device_id,
        )
        db.session.add(data)
        db.session.commit()

    def updateSettings(self, new_settings):
        """Raw method for updating a device's settings"""

        if self.device is None:
            raise Exception(f"Cannot update settings device before loading (id {self.device_id})")

        self.device.settings.update(new_settings)

        db.session.query(Device).filter_by(id=self.device_id).update({Device.settings: self.device.settings})
        db.session.commit()

    def addRuntimeSchedule(self, time_intervals: list):
        """Add running time intervals for this device\n
            Eg. time_intervals = [(8, 11), (19, 20)] means \
                the device will run (only) in the intervals\n
                8am-11am and 7pm-8pm\n
            NOTE: the intervals MUST be disjoint"""

        self.updateSettings({"schedule": time_intervals})

    def setAlwaysOn(self, status=True):
        """Set a device to always be on, ignoring any schedule or global shutdown message"""

        self.updateSettings({"always_on": status})

    def setChannel(self, channel=None):
        """Assign a channel to a device\n
            Note that the channel can coincide with other deivces' channels,
            and all the runtime-schedule intervals will be inherited\n
            If not sure, set a diffferent channel for every device
            If the channel is not provided, a random ID will be selected"""

        if channel is None:
            channel = f"channel_{self.device.uuid}_{random.randint(0, 0xffff)}"

        self.updateSettings({"channel": channel})

    def addHandler(self, handler, kwargs):
        """Add a handler for this device to be ran at startup"""

        if type(handler) != str:
            print(f"WARNING: direct handler passed to addHandler function\
                 (it was automatically converted to str);\
                 make sure it is added in the function dispatcher in ScheduleHandlers")
            handler = handler.__name__

        self.device.settings["handlers"].update({handler: kwargs})
        self.updateSettings({})

    def removeHandlers(self):
        """Remove all startup handlers for this device"""

        self.updateSettings({"handlers": {}})

    def getData(self, page=None, per_page=None):
        queryString = f"SELECT * FROM data WHERE `device_id` = {self.device_id} "
        if page != None and per_page != None:
            offset = per_page * page
            queryString += f"LIMIT {per_page} OFFSET {offset}"

        query = text(queryString)
        cursor = db.engine.execute(query)
        data = [dict(row.items()) for row in cursor]

        return data

    # it evaluates 6 hours of data, the interval beginning at the given timestamp
    def anomalyCheck(self, timestamp):
        queryString = f"SELECT * FROM data WHERE `device_id` = {self.device_id} and `time` >= Datetime('{timestamp}') and `time` <= Datetime('{timestamp}','+6 hours') "
        query = text(queryString)
        cursor = db.engine.execute(query)

        data = [dict(row.items()) for row in cursor]
        data = [[datapoint['time'], datapoint['value']] for datapoint in data]
        anomalyDetector = AnomalyDetector(self.device_id)

        return anomalyDetector.evalAnomaly(data)

    # it predicts the consumption of the given device in the period start_time, end_time in KW
    # start_time, end_time must be strings that represents the start_time, end_time
    def predictConsumption(self, start_time:str, end_time:str):
        anomalyDetector = AnomalyDetector(self.device_id)
        
        return anomalyDetector.predictConsumption(start_time, end_time)
        
    
    # predicts if this device is using much more energy than usual, and asks the user if he forgot the device in the running state
    # prediction is valid for the last 1.5 hours of running
    def isDeviceLeftRunning(self):
        queryString = f"SELECT * FROM data WHERE `device_id` = {self.device_id} and strftime('%Y',`time`) = '2015' ORDER BY `time` DESC LIMIT 3"
        query = text(queryString)
        cursor = db.engine.execute(query)

        data = [dict(row.items()) for row in cursor]
        data = [[datapoint['time'], datapoint['value']] for datapoint in data]

        start_time = data[0][0]
        end_time = data[-1][0]

        anomalyDetector = AnomalyDetector(self.device_id)
        predictedConsumption = anomalyDetector.predictConsumption(start_time, end_time)
        if predictedConsumption > 3 * sum([float(x[1]) for x in data]):
            return "Device might be left running"
        
        return "Device seems running ok"
    
    def getMonthlyConsumption(self, year, month):
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        
        queryString = f"SELECT * FROM data WHERE `device_id` = {self.device_id} and strftime('%Y',`time`) = '{year}' and strftime('%m',`time`) = '{month}'"
        query = text(queryString)
        cursor = db.engine.execute(query)

        data = [dict(row.items()) for row in cursor]
        data = [[datapoint['time'], datapoint['value']] for datapoint in data]
        
        start_day = int(data[0][0].split(" ")[0].split("-")[2])
        end_day = int(data[-1][0].split(" ")[0].split("-")[2])

        total_consumption = sum([x[1] for x in data])
        average_consumption = total_consumption / (end_day - start_day)

        return total_consumption, average_consumption
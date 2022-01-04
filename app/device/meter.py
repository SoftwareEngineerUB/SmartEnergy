import csv
import os
import pickle
import uuid

import dateutil.parser
from matplotlib import pyplot as plt
from app.models import Data, Device, User
from app.models.db import db


class MeterData:
    def __init__(self):
        self.keys = list()
        self.all = list()
        self.by_date = dict()
        self.by_key = dict()


class Meter:
    DATE_TIME_KEY = 'Date & Time'
    IGNORED_KEYS = ['use [kW]', 'gen [kW]', DATE_TIME_KEY]

    def __init__(self, user: User, year=2016, meter_id=1):
        self.user = user
        self.year = year
        self.meter_id = 1
        self.data = MeterData()

    def exportToDatabase(self):
        devices = dict()

        with open(f"data/{self.year}/meter{self.meter_id}.csv", "r") as f:
            file_contents = csv.DictReader(f)

            for field in file_contents.fieldnames:
                if field not in Meter.IGNORED_KEYS:
                    device = db.session.query(Device).filter_by(user_id=self.user.id, alias=field).first()
                    if device is None:
                        device = Device(
                            alias=field,
                            uuid=uuid.uuid4(),
                            description=field + ' mock device',
                            status=True,
                            settings=dict(),
                            user_id=self.user.id,
                        )
                        db.session.add(device)
                    devices[field] = device

            for row in file_contents:
                for key in row.keys():
                    data = Data(
                        time=row[Meter.DATE_TIME_KEY],
                        value=row[key],
                        device_id=devices[key].id,
                    )
                    db.session.add(data)

            db.session.commit()

    def plotKey(self, key):
        if key not in self.data.keys:
            return
        x = [dateutil.parser.parse(v) for v in self.data.by_key[self.DATE_TIME_KEY]]
        y = self.data.by_key[key]
        # plotting the points
        plt.plot(x, y)
        plt.xlabel('Date')
        plt.ylabel(key)
        plt.show()


if __name__ == "__main__":
    pass

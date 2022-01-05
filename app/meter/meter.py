import csv
import uuid

import dateutil.parser
from matplotlib import pyplot as plt

from app.meter.device import DeviceObject
from app.models import Data, Device, User
from app.models.db import db


class Meter:
    DATE_TIME_KEY = 'Date & Time'
    IGNORED_KEYS = ['use [kW]', 'gen [kW]', DATE_TIME_KEY]
    EXPORT_ROW_COMMIT_SPLIT = 1000

    def __init__(self, user: User):
        self.user = user
        self.devices: list[DeviceObject] = list()
        self.loadData()

    def loadData(self):
        devices = db.session.query(Device).filter_by(user_id=self.user.id).all()
        for device in devices:
            self.devices.append(DeviceObject(self.user, device))

    @staticmethod
    def exportCsvToDatabase(user: User, year=2016, meter_id=1):
        devices = dict()
        with open(f"data/{year}/meter{meter_id}.csv", "r") as f:
            file_contents = csv.DictReader(f)

            for field in file_contents.fieldnames:
                if field not in Meter.IGNORED_KEYS:
                    device = db.session.query(Device).filter_by(user_id=user.id, alias=field).first()
                    if device is None:
                        device = Device(
                            alias=field,
                            uuid=str(uuid.uuid4()),
                            description=field + ' mock device',
                            status=True,
                            settings=dict(),
                            user_id=user.id,
                        )
                        db.session.add(device)
                    devices[field] = device
            db.session.commit()
            print(f'Finished importing devices from csv for year: {year} and meter: {meter_id}')
            print("Exporting data to database...")
            for index, row in enumerate(file_contents):
                for key in row.keys():
                    if key in devices.keys():
                        data = Data(
                            time=dateutil.parser.parse(row[Meter.DATE_TIME_KEY]),
                            value=row[key],
                            device_id=devices[key].id,
                        )
                        db.session.add(data)
                if index % Meter.EXPORT_ROW_COMMIT_SPLIT == 0:
                    db.session.commit()

            print('Finished exporting data')
            db.session.commit()

    # def plotKey(self, key):
    #     if key not in self.data.keys:
    #         return
    #     x = [dateutil.parser.parse(v) for v in self.data.by_key[self.DATE_TIME_KEY]]
    #     y = self.data.by_key[key]
    #     # plotting the points
    #     plt.plot(x, y)
    #     plt.xlabel('Date')
    #     plt.ylabel(key)
    #     plt.show()


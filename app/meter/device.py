from app.models import User, Device, Data
from app.models.db import db


class DeviceObject:

    def __init__(self, user: User, device: Device):
        self.data: list[Data] = list()
        self.device = device
        self.loadData()

    def loadData(self):
        # self.data = db.session.query(Data).filter_by(device_id=self.device.id).all()
        pass

from datetime import datetime

import dateutil.parser

from app.models import User, Device, Data
from app.models.db import db


class DeviceObject:
    def __init__(self, user: User, device_id: int):
        self.device = None
        self.user = user
        self.device_id = device_id
        self.load()

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

    def detectAnomalies(self):
        pass

from json import JSONEncoder
import uuid
from typing import Optional

import dateutil.parser

from app.models import User, Device, Data
from app.models.db import db


class DeviceObject:
    def __init__(self, user: User, device_id: int):
        self.device: Optional[Device] = None
        self.user: User = user
        self.device_id: int = device_id
        self.load()

    @staticmethod
    def create(user: User, device_json):
        device = Device(
            alias=device_json['name'],
            uuid=str(uuid.uuid4()),
            description=f"{device_json['name']} mock device",
            status=True,
            settings=dict(),
            user_id=user.id,
        )
        db.session.add(device)
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
        
        if self.device is None:
            raise Exception(f"Cannot update settings device before loading (id {self.device_id})")

        self.device.settings.update(new_settings)
        db.session.query(Device).update({Device.settings: self.device.settings})

    def detectAnomalies(self):
        pass

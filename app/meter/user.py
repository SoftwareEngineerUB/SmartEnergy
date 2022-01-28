from app.meter.device import DeviceObject
from app.models.user import User
from app.models.db import db
from app.meter.meter import Meter

class UserObject:
    def __init__(self, user:User) -> None:
        self.user = user

    # returns the model assosiacted with the devices
    def getUserDevices(self):
        meter = Meter(self.user)
        return [x for x in meter.devices]
    
    
    def getMonthlyStatistics(self, year, month):
        devices = self.getUserDevices()
        devices = [DeviceObject(self.user, device.id) for device in devices]
        
        for device in devices:
            print(device.device_id)
            total_consumption = device.getMonthlyConsumption(year, month)
            print(device.device_id, total_consumption)
            

    
        # print(devices)
        # TODO : Monthly consumption, most consuming device, mean daily consumption
        
        
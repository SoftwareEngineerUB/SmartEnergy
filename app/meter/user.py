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
    
    # returns the most consuming device, and for each device the total consumption, daily consumption
    def getMonthlyStatistics(self, year, month):
        devices = self.getUserDevices()
        devices = [DeviceObject(self.user, device.id) for device in devices]

        max_consumption = 0
        max_avg_consumption = 0
        max_id = 0

        statistics = dict()
        statistics['devices consumption'] = list()
        
        for device in devices:
            total_consumption, mean_daily_consumption = device.getMonthlyConsumption(year, month)
            
            if total_consumption > max_consumption:
                max_consumption = total_consumption
                max_avg_consumption = mean_daily_consumption
                max_id = device.device_id
            
            statistics['devices consumption'].append({
                "device name: " : device.device.alias,
                "total consumption this month (kW): " : total_consumption,
                "average daily consumption (kW): " : mean_daily_consumption,
            })

            # print(device.device_id, device.device.alias, total_consumption, mean_daily_consumption)

        statistics['most consuming device'] = {
            "device name: " : [x.device.alias for x in devices if x.device_id == max_id][0],
            "total consumption (kW): " : max_consumption,
            "aaverage daily consumption (kW): " : mean_daily_consumption 
        }

        return statistics

    


        
        
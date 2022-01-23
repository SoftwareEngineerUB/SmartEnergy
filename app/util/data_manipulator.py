
from app.meter.device import DeviceObject
import numpy as np

EXTENSION_NAME = '.pth'
CURRENT_PATH = './app/util/'
DEVICE_BASE_NAME = "device_"
TRAIN_FOLDER = "train_data/"

class DataManipulator():
    @staticmethod
    def changeDataFormat(device:DeviceObject):
        initialData = device.getData()
        device_id = str(device.device_id)

        finalData = []
        for data in initialData:
            timestamp = data['time']
            dateTimestamp = timestamp.split(" ")[0]
            hourTimestamp = timestamp.split(" ")[1]

            value = float(data['value'])
            month = int(dateTimestamp.split("-")[1])
            day = int(dateTimestamp.split("-")[2])
            hour = int(hourTimestamp.split(":")[0])

            finalData.append([month, day, hour, value])
        
        finalData = np.array(finalData, dtype=np.float64)

        with open(CURRENT_PATH + TRAIN_FOLDER + DEVICE_BASE_NAME + device_id + ".npy", 'wb') as f:
            np.save(f, finalData)   

def setDataForTrain(device:DeviceObject):
    DataManipulator.changeDataFormat(device)
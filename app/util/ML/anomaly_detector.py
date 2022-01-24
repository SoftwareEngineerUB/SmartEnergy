import numpy as np
import matplotlib.pyplot as plt
import torch as T
import copy
from tqdm import tqdm

from app.util.ML.constants import *
from app.util.ML.dataset import *


class AnomalyDetector():
    def load_model(self):
        try:
            if self.cuda:
                self.model.load_state_dict(
                    T.load(self.modelPath + self.modelName + EXTENSION_NAME))
            else:
                self.model.load_state_dict(T.load(
                    self.modelPath + self.modelName + EXTENSION_NAME, map_location=T.device('cpu')))
        except Exception as e:
            print("no model saved on the disk. Continue...")

    def save_model(self):
        T.save(self.model.state_dict(), self.modelPath +
               self.modelName + EXTENSION_NAME)

    def save_state_dict(self, state_dict):
        T.save(state_dict, self.modelPath + self.modelName + EXTENSION_NAME)

    def load_model_info(self):
        try:
            file = open(self.infoFileNamePath, "r")
            self.max_loss = float(file.readline())
            file.close()
        except:
            print("no additional data saved on the disk")

    def save_model_info(self):
        try:
            file = open(self.infoFileNamePath, "w")
            file.write(str(self.max_loss))
            file.close()
        except:
            print("Error while saving")

    def __init__(self, device_id):
        # parameter for always saving the best model
        self.safe_train = True
        # parameter for converting from KW to W
        self.mul_parameter = 1000.0
        self.verbose = False

        self.device_id = device_id
        self.modelName = "device_model_" + str(device_id)
        self.infoFileNamePath = BASE_PATH + "device_statistics/" + \
            "device_info_" + str(device_id) + ".txt"
        self.modelPath = BASE_PATH + "device_models/"
        self.cuda = GPU_ENABLED

        # params -> month, day, time
        self.model = T.nn.Sequential(
            T.nn.Linear(3, 6),
            T.nn.ReLU(),
            T.nn.Linear(6, 8),
            T.nn.ReLU(),
            T.nn.Linear(8, 10),
            T.nn.ReLU(),
            T.nn.Linear(10, 13),
            T.nn.ReLU(),
            T.nn.Linear(13, 10),
            T.nn.ReLU(),
            T.nn.Linear(10, 8),
            T.nn.ReLU(),
            T.nn.Linear(8, 6),
            T.nn.ReLU(),
            T.nn.Linear(6, 3),
            T.nn.ReLU(),
            T.nn.Linear(3, 1)
        )
        if self.cuda:
            self.model.to(DEVICE)

        self.load_model()
        self.load_model_info()

    def train(self, n_epoch, lr, logging_interval=1):
        # make the dataset
        self.dataSet = DeviceMeterDataset.createDatasets(
            self.device_id, mul_factor=self.mul_parameter)
        self.dataLoader = dict()
        for key in self.dataSet.keys():
            self.dataLoader[key] = T.utils.data.DataLoader(
                self.dataSet[key], batch_size=15000, shuffle=True)

        loss_func = T.nn.MSELoss()
        optimizer = T.optim.Adam(self.model.parameters(), lr=lr)
        best_loss = None

        for epoch in tqdm(range(0, n_epoch)):
            epoch_loss = 0.0
            for type in ['train', 'validation']:
                if type == 'validation':
                    self.model.eval()
                else:
                    self.model.train()

                for (input_data, target) in self.dataLoader[type]:

                    optimizer.zero_grad()
                    value = False
                    if type == 'train':
                        value = True
                    with T.set_grad_enabled(value):
                        output = self.model(input_data)

                        loss = loss_func(output, target)
                        epoch_loss += loss.item()

                        if type == 'train':
                            loss.backward()
                            optimizer.step()

                if epoch % logging_interval == 0:
                    if self.verbose:
                        print(type + " epoch = %4d   loss = %0.4f" %
                              (epoch, epoch_loss))
                    if self.safe_train:
                        if best_loss == None or epoch_loss < best_loss:
                            best_loss = epoch_loss
                            best_state_dict = copy.deepcopy(
                                self.model.state_dict())
                            self.save_state_dict(best_state_dict)

        if not self.safe_train:
            self.save_model()

        self.load_model()
        print("Done training")

    def eval_mean_loss(self):
        dataSet = DeviceMeterDataset.createEvalData(self.device_id)
        self.model.eval()

        loss_arr = []

        for batch in dataSet:
            current_loss = 0.0
            for datapoint in batch:
                with T.no_grad():
                    X = datapoint[:3]
                    Y = datapoint[3]
                    X = T.tensor(X, dtype=T.float32).to(DEVICE)

                    oupt = self.model(X).item()  # compute output/target
                    current_loss += abs(oupt - Y)
            loss_arr.append(current_loss / len(batch))

        total_loss = 0.0
        for loss in loss_arr:
            total_loss += loss
        mean_loss = total_loss / len(loss_arr)

        self.max_loss = 3 * mean_loss
        self.save_model_info()

    @staticmethod
    def convertDeviceData(deviceData: list([str, str]), mul_factor=1.0):
        finalData = []
        for data in deviceData:
            timestamp = data[0]
            dateTimestamp = timestamp.split(" ")[0]
            hourTimestamp = timestamp.split(" ")[1]

            value = float(data[1]) * mul_factor
            month = int(dateTimestamp.split("-")[1])
            day = int(dateTimestamp.split("-")[2])
            hour = int(hourTimestamp.split(":")[0])
            minute = int(hourTimestamp.split(":")[1])

            if minute == 30:
                hour = hour + 0.5

            finalData.append([month, day, hour, value])

        finalData = np.array(finalData, dtype=np.float64)
        return finalData

    # receives as input 12 data points representing 6 continuous hours of data. The format for a datapoint is :str(date), str(consumption)
    # it returns if there was an anomaly. Data must contain
    def evalAnomaly(self, deviceData: list([str, str])):
        self.model.eval()
        data = AnomalyDetector.convertDeviceData(
            deviceData, self.mul_parameter)

        total_loss = 0.0
        for datapoint in data:
            with T.no_grad():
                X = datapoint[:3]
                Y = datapoint[3]
                X = T.tensor(X, dtype=T.float32).to(DEVICE)
                oupt = self.model(X).item()
                print(oupt, Y)
                total_loss += abs(oupt - Y)
        total_loss /= len(data)

        if total_loss > self.max_loss:
            return True

        return False

import numpy as np
import matplotlib.pyplot as plt
import torch as T
import copy
from tqdm import tqdm

from app.models.device import Device


DEVICE = T.device("cuda:0") 
GPU_ENABLED = True

EXTENSION_NAME = '.pth'
CURRENT_PATH = './app/util/'
TRAIN_FOLDER = "train_data/"
DEVICE_BASE_NAME = "device_"


class DeviceMeterDataset(T.utils.data.Dataset):
    @staticmethod
    def createDatasets(device_id, mul_factor = 1):
        allData = np.load(CURRENT_PATH + TRAIN_FOLDER + DEVICE_BASE_NAME + str(device_id) + ".npy")
        data_length = allData.shape[0]
        used_data = data_length // 5
        increasing_factor = int(data_length * 2 / 10)

        np.random.shuffle(allData)

        ans = {
            "train": DeviceMeterDataset(allData[:used_data], mul_factor),
            "validation": DeviceMeterDataset(allData[used_data:used_data + increasing_factor], mul_factor),
            "test": DeviceMeterDataset(allData[used_data + increasing_factor:used_data + 2 * increasing_factor], mul_factor)
        }
        
        return ans
    
    # we need to generate mean error to have a comparasion basis for anomaly detections 
    @staticmethod
    def createEvalData(device_id, mul_factor = 1):
        allData = np.load(CURRENT_PATH + TRAIN_FOLDER + DEVICE_BASE_NAME + str(device_id) + ".npy")

        index = np.random.choice(allData.shape[0], 1000, replace=False)
        max_index = allData.shape[0] - 12
        index = index[index < max_index] 

        evalData = []
        for id in index:
            evalData.append(allData[id:id+12, :].copy())
        
        for data in evalData:
            data[:, 3] *= mul_factor

        return evalData

    def __init__(self, data, mul_factor = 1):
        self.allData = data
        self.allData[:, 3] *= mul_factor

        self.xy_data = T.tensor(self.allData, dtype=T.float32).to(DEVICE) 
    

    def __len__(self):
        return len(self.xy_data)
    def __getitem__(self, idx):
        data = self.xy_data[idx, :3]
        value = self.xy_data[idx, 3].reshape((1))
        return data, value

class AnomalyDetector():
    def load_model(self):
        try:
            if self.cuda:
                self.model.load_state_dict(T.load(self.modelPath + self.modelName + EXTENSION_NAME))
            else:
                self.model.load_state_dict(T.load(self.modelPath + self.modelName + EXTENSION_NAME, map_location=T.device('cpu')))
        except Exception as e:
            print("no model saved on the disk. Continue...")

    def save_model(self):
        T.save(self.model.state_dict(), self.modelPath + self.modelName + EXTENSION_NAME)

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

        self.device_id = device_id
        self.modelName = "device_model_" + str(device_id)
        self.infoFileNamePath = CURRENT_PATH + "device_statistics/" + "device_info_" + str(device_id) + ".txt"
        self.modelPath = CURRENT_PATH + "device_models/"
        self.cuda = GPU_ENABLED

        # params -> month, day, time 
        self.model =  T.nn.Sequential(
            T.nn.Linear(3, 6),
            T.nn.ReLU(),
            T.nn.Linear(6, 8),
            T.nn.ReLU(),
            T.nn.Linear(8, 6),
            T.nn.ReLU(),
            T.nn.Linear(6, 3),
            T.nn.ReLU(),
            T.nn.Linear(3, 2),
            T.nn.ReLU(),
            T.nn.Linear(2, 1),
        )
        if self.cuda:
            self.model.to(DEVICE)
        
        self.load_model()
        self.load_model_info()

    
    def train(self, n_epoch, lr, logging_interval = 1):
        # make the dataset
        self.dataSet = DeviceMeterDataset.createDatasets(self.device_id, mul_factor=self.mul_parameter)
        self.dataLoader = dict()
        for key in self.dataSet.keys():
            self.dataLoader[key] = T.utils.data.DataLoader(self.dataSet[key], batch_size=15000, shuffle=True)

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
                    print(type + " epoch = %4d   loss = %0.4f" % (epoch, epoch_loss))
                    if self.safe_train:
                        if best_loss == None or epoch_loss < best_loss:
                            best_loss = epoch_loss
                            best_state_dict = copy.deepcopy(self.model.state_dict())
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

        self.max_loss = 1.5 * mean_loss 
        self.save_model_info()

    @staticmethod
    def convertDeviceData(deviceData:list([str, str])):
        finalData = []
        for data in deviceData:
            timestamp = data[0]
            dateTimestamp = timestamp.split(" ")[0]
            hourTimestamp = timestamp.split(" ")[1]

            value = float(data[1])
            month = int(dateTimestamp.split("-")[1])
            day = int(dateTimestamp.split("-")[2])
            hour = int(hourTimestamp.split(":")[0])

            finalData.append([month, day, hour, value])
        
        finalData = np.array(finalData, dtype=np.float64)
        return finalData

    # receives as input 12 data points representing 6 continuous hours of data. The format for a datapoint is :str(date), str(consumption)
    # it returns if there was an anomaly. Data must contain 
    def evalAnomaly(self, deviceData:list([str, str])):
        self.model.eval()
        data = AnomalyDetector.convertDeviceData(deviceData)

        total_loss = 0.0
        for datapoint in data:
            with T.no_grad():
                X = datapoint[:3]
                Y = datapoint[3]
                X = T.tensor(X, dtype=T.float32).to(DEVICE) 
                oupt = self.model(X).item()  

                total_loss += abs(oupt - Y)
        total_loss /= len(data)

        if total_loss > self.max_loss:
            return True
        
        return False


def main():
    anomalyDetector = AnomalyDetector(1)
    anomalyDetector.train(100, 1e-1, 2)
    anomalyDetector.train(300, 1e-2, 2)
    anomalyDetector.train(350, 5 * 1e-3, 2)
    anomalyDetector.eval_mean_loss()

if __name__ == "__main__":
    main()

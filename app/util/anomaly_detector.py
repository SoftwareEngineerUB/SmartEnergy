import numpy as np
import matplotlib.pyplot as plt
import torch as T
import copy
from tqdm import tqdm

from app.meter.device import DeviceObject

DEVICE = T.device("cuda:0") 
EXTENSION_NAME = '.pth'

class DataManipulator():
    @staticmethod
    def saveDataFromDB(device:DeviceObject):
        # TODO : to refactor this 
        initialData = device.getData()
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
        # print(os.getcwd())
        with open('./app/util/deviceData.npy', 'wb') as f:
            np.save(f, finalData)

class DeviceMeterDataset(T.utils.data.Dataset):
    def __init__(self, mul_factor = 1, data_size = 20000):
        # TODO: refactor the loading procedure
        self.allData = np.load('./app/util/deviceData.npy')
        self.allData[:, 3] *= mul_factor

        index = np.random.choice(self.allData.shape[0], data_size, replace=False)
        finalData = self.allData[index]
        finalData = np.array(finalData, dtype=np.float64)
        
        self.xy_data = T.tensor(finalData, dtype=T.float32).to(DEVICE) 
    
    def refreshData(self, data_size = 20000):
        index = np.random.choice(self.allData.shape[0], data_size, replace=False)
        finalData = self.allData[index]
        finalData = np.array(finalData, dtype=np.float64)
        
        self.xy_data = T.tensor(finalData, dtype=T.float32).to(DEVICE) 

    def __len__(self):
        return len(self.xy_data)
    def __getitem__(self, idx):
        xy = self.xy_data[idx]
        return xy

# month, day, hour_of_day, consumption
class Model(T.nn.Module):  # 4-3-2-3-4
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = T.nn.Linear(4, 6)
        self.fc2 = T.nn.Linear(6, 8)
        self.fc3 = T.nn.Linear(8, 6)
        self.fc4 = T.nn.Linear(6, 4)
        self.fc5 = T.nn.Linear(4, 1)

    def encode(self, x):  # 4-3-2
        z = T.tanh(self.fc1(x))
        z = T.tanh(self.fc2(z))  # latent in [-1,+1]
        return z  

    def decode(self, x):  # 2-3-4
        z = T.tanh(self.fc3(x))
        z = self.fc4(z)
        z = self.fc5(z)  # we don't need a fixed range
        return z
    
    def forward(self, x):
        z = self.encode(x) 
        z = self.decode(z) 
        return z  
    

class AnomalyDetector():
    def load_model(self):
        try:
            if self.cuda:
                self.autoenc.load_state_dict(T.load(self.modelPath + self.modelName + EXTENSION_NAME))
            else:
                self.autoenc.load_state_dict(T.load(self.modelPath + self.modelName + EXTENSION_NAME, map_location=T.device('cpu')))
        except Exception as e:
            print("no model saved on the disk. Continue...")

    def save_model(self):
        T.save(self.autoenc.state_dict(), self.modelPath + self.modelName + EXTENSION_NAME)

    def save_state_dict(self, state_dict):
        T.save(state_dict, self.modelPath + self.modelName + EXTENSION_NAME)

    def __init__(self, modelName:str):
        # parameter for always saving the best model
        self.safe_train = True
        # parameter for converting from KW to W
        self.mul_parameter = 1000.0

        self.modelName = modelName
        self.modelPath = "./app/util/device_models/"
        self.cuda = True

        self.autoenc =  Model()
        if self.cuda:
            self.autoenc.to(DEVICE)
        
        self.load_model()
        # TODO : refactor
        self.dataSet = DeviceMeterDataset(self.mul_parameter)
        self.dataLoader = T.utils.data.DataLoader(self.dataSet, batch_size=4096, shuffle=True)
    
    def train(self, n_epoch, lr, logging_interval = 1):
        loss_func = T.nn.MSELoss()
        optimizer = T.optim.Adam(self.autoenc.parameters(), lr=lr)
        best_loss = None
        self.autoenc.train()   # set mode

        for epoch in tqdm(range(0, n_epoch)):
            epoch_loss = 0.0
            for (batch_idx, batch) in enumerate(self.dataLoader):
                X = batch  # inputs
                Y = batch  # targets (same as inputs)
                #print(Y.shape)
                Y = Y[:, 3].reshape((Y.shape[0], 1))
                #print(Y.shape)
                # print(Y)
                #input()
                # TODO ideea : 

                optimizer.zero_grad()                # prepare gradients
                oupt = self.autoenc(X)                   # compute output/target
                loss_val = loss_func(oupt, Y)  # a tensor
                epoch_loss += loss_val.item()  # accumulate for display
                loss_val.backward()            # compute gradients
                optimizer.step()                     # update weights


            if epoch % logging_interval == 0:
                print("epoch = %4d   loss = %0.4f" % (epoch, epoch_loss))
                if self.safe_train:
                    if best_loss == None or epoch_loss < best_loss:
                        best_loss = epoch_loss
                        best_state_dict = copy.deepcopy(self.autoenc.state_dict())
                        self.save_state_dict(best_state_dict)

        if not self.safe_train:
            self.save_model()

        # loading the best model so far
        self.load_model()
        print("Done training")

    def eval_total_loss(self):
        self.autoenc.eval()
        self.dataSet.refreshData()
        self.dataLoader = T.utils.data.DataLoader(self.dataSet, batch_size=4096, shuffle=True)
        loss_func = T.nn.MSELoss()
        total_loss = 0.0 

        for (batch_idx, batch) in enumerate(self.dataLoader):
            with T.no_grad():
                X = batch  # inputs
                Y = batch  # targets (same as inputs)
                #print(Y.shape)
                Y = Y[:, 3].reshape((Y.shape[0], 1))

                oupt = self.autoenc(X)  # compute output/target
                loss_val = loss_func(oupt, Y)  # a tensor
                total_loss += loss_val.item()  # accumulate for display
        
        print(f"Total loss for this dataset is {total_loss}")


    # receives as input a list, each element is date(str), consumption(str) of the given device 
    # it returns the mean loss 
    def eval_loss(self, deviceData:list([str, str])):
        self.autoenc.eval()

        with T.no_grad():
            pass

def getDataFromDb(device:DeviceObject):
    DataManipulator.saveDataFromDB(device)

def main():
    anomalyDetector = AnomalyDetector("third")
    # anomalyDetector.train(1000, 1e-2, 50)
    # anomalyDetector.train(1000, 1e-3, 50)
    anomalyDetector.eval_loss()

if __name__ == "__main__":
    main()

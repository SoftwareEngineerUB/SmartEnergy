import csv
import os
import pickle

import dateutil.parser
from matplotlib import pyplot as plt


class MeterData:
    def __init__(self):
        self.keys = list()
        self.all = list()
        self.by_date = dict()
        self.by_key = dict()


class Meter:
    def __init__(self, year=2016, meter_id=1):
        self.data = MeterData()
        self.loadData(year, meter_id)
        print(self.data)

    def loadData(self, year, meter_id):
        pickle_file_path = f'data/pickles/{year}_{meter_id}.pkl'
        if os.path.exists(pickle_file_path):
            dbfile = open(pickle_file_path, 'rb')
            self.data = pickle.load(dbfile)
            dbfile.close()
            return
        with open(f"data/{year}/meter{meter_id}.csv", "r") as f:
            file_contents = csv.DictReader(f)
            for row in file_contents:
                self.data.all.append(row)
                date = dateutil.parser.parse(row['Date & Time'])
                self.data.by_date[str(date)] = row
                for key in row.keys():
                    if key not in self.data.by_key.keys():
                        self.data.by_key[key] = list()
                    self.data.by_key[key].append(row[key])
            if len(self.data.all) > 0:
                self.data.keys = list(self.data.all[0].keys())
        # Its important to use binary mode
        dbfile = open(pickle_file_path, 'ab')
        pickle.dump(self.data, dbfile)
        dbfile.close()

    def plotKey(self, key):
        if key not in self.data.keys:
            return
        x = [dateutil.parser.parse(v) for v in self.data.by_key['Date & Time']]
        y = self.data.by_key[key]
        # plotting the points
        plt.plot(x, y)
        plt.xlabel('Date')
        plt.ylabel(key)
        plt.show()


meter = Meter()
# meter.plotKey("FurnaceHRV [kW]")

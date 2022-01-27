
import csv 
from datetime import datetime
from datetime import timedelta

from sqlalchemy import column


for index in range(1, 4):
    for year in range(2014, 2017):
        if year == 2014 and index == 3:
            continue

        readerData = []
        with open(f'./demo-data/{year}/meter' + str(index) + '.csv', newline='') as read_f:
            reader = csv.reader(read_f)
            for row in reader:
                readerData.append(row)

        data_len = len(readerData)

        timestamp1 = int(readerData[1][0].split(" ")[1].split(":")[1])
        timestamp2 = int(readerData[2][0].split(" ")[1].split(":")[1])
        step_size = None
        if timestamp2 - timestamp1 == 30:
            continue
        else:
            step_size = 30 // (timestamp2 - timestamp1)
        
    
        with open(f'./demo-data/{year}/meter' + str(index) +  '_new.csv', mode ='w') as write_f:
            try:
                writer = csv.writer(write_f, delimiter=',')
                writer.writerow(readerData[0])

                for line_index in range(1, len(readerData), step_size):
                    line_to_insert = readerData[line_index]
                    for column_index in range(1, len(line_to_insert)):
                        line_to_insert[column_index] = float(line_to_insert[column_index])

                    # print(line_to_insert)
                    for next_index in range(1, step_size):
                        for column_index in range(1, len(line_to_insert)):
                            if line_index + next_index < len(readerData):
                                line_to_insert[column_index] += float(readerData[line_index + next_index][column_index])

                    # print(line_to_insert)
                    # input()
                    writer.writerow(line_to_insert)
            except Exception as e:
                print(e)
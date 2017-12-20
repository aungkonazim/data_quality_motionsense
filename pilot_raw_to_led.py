import numpy as np
import pandas as pd
import pickle
def decode_1(array):
    accel_x = int(array[0]+array[1],16)
    accel_y = int(array[2]+array[3],16)
    accel_z = int(array[4]+array[5],16)
    ecg_led_1 = int(array[7]+array[8],16)
    ecg_led_2 = int(array[10]+array[11],16)
    ecg_led_3 = int(array[13]+array[14],16)

    return ecg_led_1, ecg_led_2, ecg_led_3


ids  = [2952,2972,2981,2983,3029]
for j1,id in enumerate(ids):
    print(id)
    filenameraw = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[j1]) + '\\RAW+MOTION_SENSE_HRV+LEFT_WRIST.csv'
    filename = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[j1]) + '\\data_final1.p'
    data2 = pd.read_csv(filenameraw, names =[str(i) for i in range(1,23)]) # name of the input csv file which contains raw data.
    data = data2[[str(i) for i in range(3,23)]]
    time = data2['1']
    time = time.as_matrix()
    data = data.as_matrix()

    data = data.astype(np.uint8)

    data1 = [['0' for i in range(20)] for j in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data[0])):
            s=str(hex(data[i][j])).split('x')[-1]
            if len(s) < 2:
                s = '0' + s
            data1[i][j] = s

    data_final = []
    for i in range(len(data1)):
        x1,x2,x3 = decode_1(data1[i])
        data_final.append([time[i],x1,x2,x3])
    pickle.dump(data_final,open( filename, "wb" ))
    del data1
    del data2
    del data
    del time


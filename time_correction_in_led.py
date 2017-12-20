import numpy as np
import pandas as pd
import pickle

ids = [2952,2972,2981,2983,3029]
for i,id in enumerate(ids):
    filename = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\data_final.p'
    filenamecsv = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\led.csv'
    data_final = pickle.load(open( filename, "rb" ))
    time = []
    led1 = []
    led2 = []
    led3 = []
    for index,element in enumerate(data_final):
        time.append(element[0])
        led1.append(element[1])
        led2.append(element[2])
        led3.append(element[3])
    time1 = []
    time_diff = [1] + list(np.diff(time))
    time_diff = np.array(time_diff)
    print(np.unique(time_diff)[0:20])
    j=0
    while(j<len(time_diff)):
        k = j
        while(k<len(time_diff)-1 and time_diff[k]<67):
            time[k] = time[j] + (k-j)*(1000/15)
            k = k + 1
        time[k] = time[j] + (k-j)*(1000/15)
        j = k+1
    data = pd.DataFrame({'time':time,'led1':led1,'led2':led2,'led3':led3},index=None)
    data.to_csv(filenamecsv,sep=',',float_format="%12d")
    del data
    del data_final
    del time
    del led1
    del led2
    del led3
    
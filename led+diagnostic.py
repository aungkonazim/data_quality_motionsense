import numpy as np
import pandas as pd

ids =[2952,2972,2983,3029]
for i,id in enumerate(ids):
    df = pd.read_table('C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\diagnostic\\'+ str(ids[i])+ 'motionsense_left_diagnostic.txt',sep=',',names=['start','end','label'])
    start = list(df['start'])
    label = list(df['label'])
    filenamecsv = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\led.csv'
    filenametimecsv = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\led.csv'
    filenamegoodcsv = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\good_data_final.csv'
    data = pd.read_csv(filenamecsv, names =['index','led1','led2','led3','time'])
    led1 = list(data['led1'])
    led2 = list(data['led2'])
    led3 = list(data['led3'])
    data = pd.read_csv(filenametimecsv, names =['index','time'])
    time = list(data['time'])
    j = 0
    good = []
    while(j<len(start)):
        if(label[j]==9):
            start1 = start[j]
            k = j
            while(label[k]==9):
                k=k+1
            end1 = start[k]
            good.append([start1,end1])
            j=k
        j=j+1
    time = np.array(time)
    led1 = np.array(led1)
    led2 = np.array(led2)
    led3 = np.array(led3)
    time_final = []
    led1_final =[]
    led2_final = []
    led3_final = []
    for index,element in enumerate(good):
        st = good[index][0]
        et = good[index][1]
        y = np.where(time>=st)
        z = np.where(time<=et)
        index1 = np.intersect1d(y,z)
        if len(index1)>0:
            time_final.extend(time[index1])
            led1_final.extend(led1[index1])
            led2_final.extend(led2[index1])
            led3_final.extend(led3[index1])
    data = pd.DataFrame({'time':time_final,'led1':led1_final,'led2':led2_final,'led3':led3_final},index=None)
    data.to_csv(filenamegoodcsv,sep=',',float_format="%12d")
    del data
    del led1
    del led2
    del led3
    del time
    del df

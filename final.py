import numpy as np
import pandas as pd
from scipy import signal
from collections import Counter
def filtering(x,fs):
    x = signal.detrend(x)
    b = signal.firls(129,[0,0.6*2/fs,0.7*2/fs,3*2/fs,3.5*2/fs,1],[0,0,1,1,0,0],[100*0.02,0.02,0.02])
    return signal.convolve(x,b,'valid')

def quality(l1,l2,l3,u1,u2,u3):
    if np.std(u1)<20 and np.std(u2) < 20 and np.std(u3) < 20:
        print("std")
        return False
    m1 = np.mean(l1)
    m2 = np.mean(l2)
    m3 = np.mean(l3)
    if(len(l1)<40):
        print("less data")
        return False
    if len(np.where(l1<5000)[0]) > .34*len(l1) and len(np.where(l2<5000)[0]) > .34*len(l2) and len(np.where(l3<2000)[0]) > .34*len(l3):
        print("outlier")
        return False
    if (sum(l1)+sum(l2)+sum(l3))/(3*len(l1)) < 9000:
        print("sum/len")
        return False
    if not (m3<m1 and m1<m2 and m3<m2):
        print("chronology")
        return False
    if m1-m3<3000 and m2-m1<3000:
        return False
    # if (m2*1.6370-4171)- m1 >= 0:
    #     print('m2 m1 equation')
    #     return False
    # if (m2*1.24291-280) - m3 >= 0:
    #     print("m2 m1 equation")
    #     return False
    return True

ids =[2983]
for i,id in enumerate(ids):
    df = pd.read_table('C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\diagnostic\\'+ str(ids[i])+ 'motionsense_left_diagnostic.txt',sep=',',names=['start','end','label'])
    start = np.array(df['start'])
    end = np.array(df['end'])
    label = np.array(df['label'])
    filenamecsv = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\led.csv'
    filenametimecsv = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\led.csv'
    filenamegoodcsv = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\good_data_final.csv'
    data = pd.read_csv(filenamecsv, names =['index','led1','led2','led3','time'])
    led1 = np.array(data['led1'][128:])
    led2 = np.array(data['led2'][128:])
    led3 = np.array(data['led3'][128:])
    led11 = np.array(filtering(data['led1'],10))
    led22 = np.array(filtering(data['led2'],10))
    led33 = np.array(filtering(data['led3'],10))
    # data = pd.read_csv(filenametimecsv, names =['index','time'])
    time = np.array(data['time'][128:])
    print(len(time),len(led1),len(led11))
    temp = np.where((label !=18) & (label !=20))
    temp = list(temp[0])
    for j1,elem in enumerate(temp):
        j=elem
        temp_label = []
        for k in range(6):
            index = np.where((time>=start[j]+k*10000) & (time<=start[j]+(k+1)*10000))[0]
            if len(index)>0:
                l1 = led1[index]
                l2 = led2[index]
                l3 = led3[index]
                u1 = led11[index]
                u2  = led22[index]
                u3 = led33[index]
                print(len(l1))
                if quality(l1,l2,l3,u1,u2,u3):
                    temp_label.append(9)
                else:
                    temp_label.append(8)
        if len(index) > 0:
            label[j] = Counter(temp_label).most_common()[0][0]
        # print(j1)

    final = []
    for k in range(len(start)):
        final.append([start[k],end[k],label[k]])

    filenametxt = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\diagnostic\\'+ str(ids[i])+ 'motionsense_left_diagnostic_new.txt'
    np.savetxt(filenametxt,final,delimiter=',',fmt="%13d")


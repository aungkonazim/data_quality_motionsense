import scipy.io as sio
import datetime
import numpy as np
import pandas as pd
from collections import Counter
import pytz
from matplotlib.dates import date2num
import matplotlib.pyplot as plt


ids = [3100,3101,3054,3096,3098]
def takeClosest(num,collection):
    return min(collection,key=lambda x:abs(x-num))

dataf = {}
dataf['ParticipantID'] = []
dataf['Date'] = []
dataf['SENSOR DISCONNECTED'] = []
dataf['INSUFFICIENT DATA'] = []
dataf['SENSOR OFF BODY'] = []
dataf['SENSOR ON BODY'] = []
dataf['SENSOR POWERED OFF'] = []
dataf['PHONE POWERED OFF LABEL'] = []


for i in range(len(ids)):
    df = pd.read_table('C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\diagnostic\\'+ str(ids[i])+ 'motionsense_right_diagnostic.txt',sep=',',names=['start','end','label'])
    start1 = list(df['start'])
    label1 = list(df['label'])
    print(len(start1))
    print(len(np.unique(start1)))
    date = []
    for index,element in enumerate(start1):
        date.append(int(datetime.datetime.fromtimestamp(float(element) / 1000.0, pytz.timezone('US/Central')).strftime('%Y-%m-%d %H:%M:%S')[8:10]))

    # start2 = []
    # label2 = []
    # unique_dates = []
    # start2.append([])
    # label2.append([])
    # start_date = date[0]
    # unique_dates.append(date[0])
    # u = 0
    # for ing,dt in enumerate(date):
    #     if dt==start_date:
    #         start2[u].append(start1[ing])
    #         label2[u].append(label1[ing])
    #     else:
    #         start2.append([])
    #         label2.append([])
    #         unique_dates.append(dt)
    #         start_date = dt
    #         u = u + 1
    #         start2[u].append(start1[ing])
    #         label2[u].append(label1[ing])
    # # start3 = []
    # label3 = []
    # unique_dates1 = []
    # for ing,lb in enumerate(label2):
    #     print(np.unique(lb))
    #     if len(np.unique(lb)) != 1:
    #         start3.append(start2[ing])
    #         unique_dates1.append(unique_dates[ing])
    #         label3.append(lb)
    #
    # print(len(label3))
    # print(len(start3))
    # print(unique_dates1)
    #
    # label2 = label3
    # start2 = start3
    # unique_dates = unique_dates1


    # # print(date)
    date_diff = np.diff(date)
    date_diff = [0] + date_diff
    ind = np.argwhere(date_diff != 0)

    start = 0
    start2 = []
    label2 = []

    unique_dates = []
    unique_dates.append(date[0])
    p1 = 0
    start = date[0]
    while p1<len(date):
        if date[p1] != start:
            unique_dates.append(date[p1])
            start = date[p1]
        p1 = p1 + 1


    for index,element in enumerate(ind):
        start2.append(start1[start:element[0]+1])
        label2.append(label1[start:element[0]+1])
        start = element[0]+1

    start2.append(start1[start:])
    label2.append(label1[start:])

    # for index in range(len(label2)):
    #     label2[index] = label2[index][len(label2[index])//2:-1]
    #     start2[index] = start2[index][len(start2[index])//2:-1]




    for index,tsarray in enumerate(start2):
        labelarray = []
        tsarray_final = []
        lbarray = label2[index]
        for index1,label in enumerate(label2[index]):
            if label == 4:
                labelarray.append('SENSOR DISCONNECTED')
            if label == 6:
                labelarray.append('INSUFFICIENT DATA')
            if label == 8:
                labelarray.append('Sensor off Body')
            if label == 9:
                labelarray.append('Sensor on Body')
            if label == 10:
                labelarray.append('Improper Attachment')
            if label == 12:
                labelarray.append('Delay In Attachment')
            if label == 14:
                labelarray.append('SENSOR_BATTERY_DOWN')
            if label == 16:
                labelarray.append('PHONE_BATTERY_DOWN_LABEL')
            if label == 18:
                labelarray.append('SENSOR_POWERED_OFF')
            if label == 20:
                labelarray.append('PHONE_POWERED_OFF_LABEL')
            if label == 22:
                labelarray.append('Acceptable Data')

        # df = pd.DataFrame({'timestamp':tsarray,                           'q_sample':lbarray})
        # df.to_csv('C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\diagnostic\\'+str(unique_dates[index])+'_quality_'+ str(ids[i])+'ecg.csv',sep=',',index=False,header=False)

    print(len(unique_dates))
    print(len(label2))
    stat = [[0 for r1 in range(11)] for r in range(len(unique_dates))]

    for k in range(len(label2)):
        cnt = Counter(label2[k])
        stat[k][0] = cnt[4]*(1/60)  if 4 in cnt.keys() else 0 # SENSOR DISCONNECTED
        stat[k][1] = cnt[6]/60 if 6 in cnt.keys() else 0 # INSUFFICIENT DATA
        stat[k][2] = cnt[8]*(1/60) if 8 in cnt.keys() else 0 # SENSOR_OFF_BODY
        stat[k][3] = cnt[9]/60 if 9 in cnt.keys() else 0 # SENSOR_ON_BODY
        stat[k][4] = cnt[10]*(1/60)  if 10 in cnt.keys() else 0 # IMPROPER_ATTACHMENT
        stat[k][5] = cnt[12]/60 if 12 in cnt.keys() else 0 # DELAY_IN_ATTACHMENT
        stat[k][6] = cnt[14]*(1/60) if 14 in cnt.keys() else 0 # SENSOR_BATTERY_DOWN
        stat[k][7] = cnt[16]/60 if 16 in cnt.keys() else 0 # PHONE_BATTERY_DOWN_LABEL
        stat[k][8] = cnt[18]/60 if 18 in cnt.keys() else 0 # PHONE_BATTERY_DOWN_LABEL
        stat[k][9] = cnt[20]*(1/60) if 20 in cnt.keys() else 0 # SENSOR_BATTERY_DOWN
        stat[k][10] = cnt[22]/60 if 22 in cnt.keys() else 0 # PHONE_BATTERY_DOWN_LABEL

    SENSOR_UNAVAILABLE = 4
    DATA_LOST = 6
    SENSOR_OFF_BODY = 8
    SENSOR_ON_BODY = 9
    IMPROPER_ATTACHMENT = 10
    DELAY_IN_ATTACHMENT = 12
    SENSOR_BATTERY_DOWN = 14
    PHONE_BATTERY_DOWN_LABEL = 16
    SENSOR_POWERED_OFF = 18
    PHONE_POWERED_OFF_LABEL = 20
    ACCEPTABLE_DATA = 22

    data = {}
    data['Date'] = []
    data['SENSOR DISCONNECTED'] = []
    data['INSUFFICIENT DATA'] = []
    data['SENSOR OFF BODY'] = []
    data['SENSOR ON BODY'] = []
    data['SENSOR POWERED OFF'] = []
    data['PHONE POWERED OFF LABEL'] = []

    for m in range(len(stat)):
        data['Date'].append(unique_dates[m])
        data['SENSOR DISCONNECTED'].append(stat[m][0])
        data['INSUFFICIENT DATA'].append(stat[m][1])
        data['SENSOR OFF BODY'].append(stat[m][2])
        data['SENSOR ON BODY'].append(stat[m][3])
        data['SENSOR POWERED OFF'].append(stat[m][8])
        data['PHONE POWERED OFF LABEL'].append(stat[m][9])

    # df = pd.DataFrame(data)
    # # bar = Bar(df,
    #           values=blend('SENSOR DISCONNECTED','INSUFFICIENT DATA','SENSOR OFF BODY','SENSOR ON BODY','IMPROPER ATTACHMENT',
    #                        'DELAY IN ATTACHMENT','SENSOR BATTERY DOWN','PHONE BATTERY DOWN LABEL',
    #                        'SENSOR POWERED OFF','PHONE POWERED OFF LABEL','ACCEPTABLE DATA',
    #                        name='Hours', labels_name='medal'),
    #           label=cat(columns='Date', sort=False),
    #           stack=cat(columns='medal', sort=False),
    #           color=color(columns='medal', sort=False),
    #           legend='top_left',
    #           title="Motion Sense Left Wrist Accelerometer data quality of participant id " + str(ids[i]),width = 800)
    # # output_file('Motionsense_LW_DataQuality_of_'+str(ids[i])+".html", title="ACL_BAR_Plot")
    #
    # show(bar)

    dataf['SENSOR DISCONNECTED'] = dataf['SENSOR DISCONNECTED'] + data['SENSOR DISCONNECTED']
    dataf['INSUFFICIENT DATA'] = dataf['INSUFFICIENT DATA'] + data['INSUFFICIENT DATA']
    dataf['SENSOR OFF BODY'] = dataf['SENSOR OFF BODY'] + data['SENSOR OFF BODY']
    dataf['SENSOR ON BODY'] = dataf['SENSOR ON BODY'] + data['SENSOR ON BODY']
    dataf['SENSOR POWERED OFF'] = dataf['SENSOR POWERED OFF'] + data['SENSOR POWERED OFF']
    dataf['PHONE POWERED OFF LABEL'] = dataf['PHONE POWERED OFF LABEL'] + data['PHONE POWERED OFF LABEL']
    dataf['Date'] = dataf['Date'] + data['Date']
    dataf['ParticipantID'] = dataf['ParticipantID'] + [ids[i] for f in range(len(data['Date']))]

df = pd.DataFrame(dataf)

df.to_excel('motionsense_right_for_all_dec7.xlsx')

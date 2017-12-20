import scipy.io as sio
import datetime
import json
import numpy as np
import pandas as pd
from bokeh.charts import Bar, output_file, show
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform
from bokeh.plotting import hplot,figure
import csv
from collections import Counter

ids = [2952,2959,2972,2981]

def takeClosest(num,collection):
    return min(collection,key=lambda x:abs(x-num))

dataf = {}
dataf['ParticipantID'] = []
dataf['Date'] = []
dataf['ACCEPTABLE'] = []
dataf['UNACCEPTABLE'] = []
dataf['Total'] = []

for i in range(len(ids)):
    df = pd.read_table('C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\diagnostic\\'+ str(ids[i])+ 'motionsense_right_diagnostic.txt',sep=',',names=['start','end','label'])
    start1 = list(df['start'])
    label1 = list(df['label'])
    date = []
    for index,element in enumerate(start1):
        date.append(int(datetime.datetime.fromtimestamp(element/1000).strftime('%Y-%m-%d %H:%M:%S')[8:10]))
    date_diff = np.diff(date)
    date_diff = [0] + date_diff
    ind = np.argwhere(date_diff != 0)
    start = 0
    start2 = []
    label2 = []

    for index,element in enumerate(ind):
        start2.append(start1[start:element[0]+1])
        label2.append(label1[start:element[0]+1])
        start = element[0]+1

    start2.append(start1[start:element[0]+1])
    label2.append(label1[start:element[0]+1])

    unique_dates = []
    unique_dates.append(date[0])
    p1 = 0
    start = date[0]
    while p1<len(date):
        if date[p1] != start:
            unique_dates.append(date[p1])
            start = date[p1]
        p1 = p1 + 1
    stat = [[0 for r1 in range(2)] for r in range(len(unique_dates))]

    for k in range(len(label2)):
        cnt = Counter(label2[k])
        stat[k][0] = cnt[9]*(1/60)
        stat[k][1] = (len(label2[k])-cnt[9]-cnt[8]-cnt[20]-cnt[6])/60


    data = {}
    data['ACCEPTABLE'] = []
    data['UNACCEPTABLE'] = []
    data['Date'] = []
    for m in range(len(stat)):
        data['ACCEPTABLE'].append(stat[m][0])
        data['UNACCEPTABLE'].append(stat[m][1])
        data['Date'].append(unique_dates[m])

    data['Total'] = [data['ACCEPTABLE'][k] + data['UNACCEPTABLE'][k] for k in range(len(data['Date']))]
    df = pd.DataFrame(data)
    bar = Bar(df,
              values=blend('ACCEPTABLE','UNACCEPTABLE', name='Hours', labels_name='medal'),
              label=cat(columns='Date', sort=False),
              stack=cat(columns='medal', sort=False),
              color=color(columns='medal', palette=['Green', 'Red'],
                          sort=False),
              legend='top_left',
              title="Motion Sense Right Wrist Accelerometer data quality of participant id " + str(ids[i]),width = 800)
    output_file('Motionsense_RW_DataQuality_of_'+str(ids[i])+".html", title="ACL_BAR_Plot")

    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="Date", title="Date"),
        TableColumn(field="ACCEPTABLE", title="ACCEPTABLE(Hours)"),
        TableColumn(field="UNACCEPTABLE", title="UNACCEPTABLE(Hours)"),
        TableColumn(field="Total", title="Total(Hours)")
    ]
    data_table = DataTable(source=source, columns=columns, width=500, height=400)

    show(hplot(bar,vform(data_table)))

    dataf['ACCEPTABLE'] = dataf['ACCEPTABLE'] + data['ACCEPTABLE']
    dataf['UNACCEPTABLE'] = dataf['UNACCEPTABLE'] + data['UNACCEPTABLE']
    dataf['Date'] = dataf['Date'] + data['Date']
    dataf['Total'] = dataf['Total'] + data['Total']
    dataf['ParticipantID'] = dataf['ParticipantID'] + [ids[i] for f in range(len(data['Total']))]

df = pd.DataFrame(dataf)

df.to_csv('acl_right.csv',sep=',')

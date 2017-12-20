
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
from bokeh.plotting import hplot
import csv
import pytz

ids = [2952,2959,2972,2981,2900,2901]

dataf = {}
dataf['ParticipantID'] = []
dataf['Date'] = []
dataf['ACCEPTABLE'] = []
dataf['UNACCEPTABLE'] = []
dataf['Total'] = []

for i in range(len(ids)):
    dirt = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\ecg_temp.mat'
    ecg = sio.loadmat(dirt)
    x = ecg['x'][0]
    y = ecg['y'][0]
    qx = ecg['qx'][0]
    qy = ecg['qy'][0]
    # date = []
    # for index,element in enumerate(x):
    #     date.append(int(datetime.datetime.fromtimestamp(element/1000,pytz.timezone('US/Central')).strftime('%Y-%m-%d %H:%M:%S')[8:10]))
    # with open(str(ids[i])+ "date.json", 'w') as f:
    #     json.dump(date, f)
    with open(str(ids[i])+ "date.json", 'r') as f:
        date = json.load(f)
    date_diff = np.diff(date)
    date_diff = [0] + date_diff
    ind = np.argwhere(date_diff != 0)
    start = 0
    timestamp = []
    sample = []
    qts = []
    qsample = []
    for index,element in enumerate(ind):
        timestamp.append(x[start:element[0]+1])
        sample.append(y[start:element[0]+1])
        qts.append(qx[start:element[0]+1])
        qsample.append(qy[start:element[0]+1])
        start = element[0]+1
    timestamp.append(x[start:-1])
    sample.append(y[start:-1])
    qts.append(qx[start:-1])
    qsample.append(qy[start:-1])
    stat = [[0 for r1 in range(3)] for r in range(len(list(set(date))))]
    for k in range(len(timestamp)):
        for j in range(1,len(qsample[k])):
            if qts[k][j]- qts[k][j-1] > 20:
                prev = 20
            else:
                prev = qts[k][j]- qts[k][j-1]
            if qsample[k][j]==0:
                stat[k][0] = stat[k][0] + (prev)/(1000*3600)
            if qsample[k][j]==2:
                stat[k][1] = stat[k][1] + (prev)/(1000*3600)
            if qsample[k][j]==3:
                stat[k][2] = stat[k][2] + (prev)/(1000*3600)
    unique_dates = []
    unique_dates.append(date[0])
    p1 = 0
    start = date[0]
    while p1<len(date):
        if date[p1] != start:
            unique_dates.append(date[p1])
            start = date[p1]
        p1 = p1 + 1
    data = {}
    data['ACCEPTABLE'] = []
    data['UNACCEPTABLE'] = []
    data['Date'] = []
    for m in range(len(stat)):
        data['ACCEPTABLE'].append(stat[m][0])
        data['UNACCEPTABLE'].append(stat[m][1]+stat[m][2])
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
              title="ECG data quality of participant id " + str(ids[i]),width = 800)

    output_file('ECG_DataQuality_of_'+str(ids[i])+".html", title="ECG_BAR_Plot")

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

df.to_excel('ECG.xlsx')











# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 03:20:37 2017

@author: aungkon
"""

import numpy as np
from scipy import signal
import pandas as pd




def decodenew(element):
    num = ((element[18] & 0x03)<<8) + (element[19] & 0xff)
    x3 = ((element[16] & 0x0f)<<14) + ((element[17] & 0xff)<<6) + (element[18] & 0xfc)
    x2 = ((element[14] & 0x3f)<<12) + ((element[15] & 0xff)<<4) + (element[16] & 0xf0)
    x1 = ((element[12] & 0xff)<<10) + ((element[13] & 0xff)<<2) + (element[14] & 0xc0)
    return x1,x2,x3,num


def decodeold(element):
    num = ((element[18] & 0x3)<<8) + (element[19] & 0xff)
    x3 = ((element[16] & 0x0f)<<14) + ((element[17] & 0xff)<<6) + (element[18] & 0xfc)
    x2 = ((element[14] & 0x3f)<<12) + ((element[15] & 0xff)<<4) + (element[16] & 0xf0)
    x1 = ((element[12] & 0xff)<<10) + ((element[13] & 0xff)<<2) + (element[14] & 0x03)
    return x1,x2,x3,num

def isDatapointsWithinRange(red,infrared,green):
    a =  len(np.where((red >= 14000)& (red<=170000))[0]) < .64*len(red)
    b = len(np.where((infrared >= 100000)& (infrared<=245000))[0]) < .64*len(infrared)
    c = len(np.where((green >= 800)& (green<=20000))[0]) < .64*len(green)
    if a and b and c:
        return False
    return True

def bandpassfilter(x,fs):
    """

    :param x: a list of samples
    :param fs: sampling frequency
    :return: filtered list
    """
    x = signal.detrend(x)
    b = signal.firls(129,[0,0.6*2/fs,0.7*2/fs,3*2/fs,3.5*2/fs,1],[0,0,1,1,0,0],[100*0.02,0.02,0.02])
    return signal.convolve(x,b,'valid')


def compute_quality(red,infrared,green):
    """

    :param window: a window containing list of datapoints
    :return: an integer reptresenting the status of the window 0= attached, 1 = not attached
    """

    if not isDatapointsWithinRange(red,infrared,green):
        return 1

    if np.mean(red) < 5000 and np.mean(infrared) < 5000 and np.mean(green)<5000:
        return 1

    if not (np.mean(red)>np.mean(green) and np.mean(infrared)>np.mean(red)):
        return 1

    diff = 30000
    if np.mean(red)>140000 or np.mean(red)<=30000:
        diff = 11000

    if not (np.mean(red) - np.mean(green) > diff and np.mean(infrared) - np.mean(red) >diff):
        return 1

    if np.std(bandpassfilter(red,25)) <= 5 and np.std(bandpassfilter(infrared,25)) <= 5 and np.std(bandpassfilter(green,25)) <= 5:
        return 1

    return 0
ids = [3100,3096,3054,3098]
for id in ids:
    data = pd.read_csv("C:\\Users\\aungkon\\Desktop\\jhu-pilot\\"+ str(id) +"\\left_wrist.csv")
    data = data.as_matrix()
    time = []
    for element in data:
        time.append(element[0])

    data = data.astype(np.uint8)
    data = data.astype(np.int32)
    red = []
    infrared = []
    green = []

    for i,element in enumerate(data):
        x1,x2,x3,num = decodenew(element[2:])
        red.append(x1)
        infrared.append(x2)
        green.append(x3)
    i=0


    red = np.array(red)
    infrared = np.array(infrared)
    green = np.array(green)
    quality = []
    while i < len(time):
        index  = np.where((time>time[i]) & (time<=time[i]+60000))[0]
        red1 = red[index]
        infrared1 = infrared[index]
        green1 = green[index]
        if len(index) > 130:
            quality.append([time[i],compute_quality(red1,infrared1,green1)])
        else:
            quality.append([time[i],1])
        if len(index)>0:
            i = index[-1]+1
        else:
            i = i + 1


    np.savetxt("C:\\Users\\aungkon\\Desktop\\jhu-pilot\\"+ str(id)+ "\\left_wrist.txt",quality,delimiter=",")
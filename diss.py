# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:58:07 2023

@author: frank
"""

import numpy as np
from matplotlib import pyplot as plt

basicHz = 256 #基频为256Hz
HzRange =np.arange(250,1648,0.5) #计算范围

def disSin(hz1,hz2,amp1,amp2):#计算两正弦波的不协和度
    high = np.where(hz1>hz2,hz1,hz2)#较高音
    low = np.where(hz1<hz2,hz1,hz2)#较低音
    s = 0.24/(0.021*low + 19)#计算公式
    diss = np.exp(-3.5*(high - low)*s)\
          -np.exp(-5.75*(high - low)*s)#计算公式
    #diss = np.where(hz1<hz2,diss,0)
    return amp1*amp2*diss#计算公式

def disSin2(hz1,hz2,amp1,amp2):#计算两正弦波的不协和度
    high = np.where(hz1>hz2,hz1,hz2)#较高音
    low = np.where(hz1<hz2,hz1,hz2)#较低音
    loud = np.where(amp1>amp2,amp1,amp2)#较响音
    quiet = np.where(amp1<amp2,amp1,amp2)#较静音
    q = high - low#计算公式
    #diss = np.exp(-0.84*q)-np.exp(-1.38*q)#计算公式
    return np.where(q<1,1,0)




def disTone(hz1,hz2):#计算两音的不协和度
    harm = np.arange(1,256+1)
    harm1 = hz1*harm#第一个音的泛音列
    harm2 = hz2*harm#第二个音的泛音列
    amp = (harm//8+1)**-1.5#强度为调和级数递减
    s1,s2 = np.meshgrid(harm1,harm2)#两列泛音的格点（方便两两计算）
    amp1,amp2 = np.meshgrid(amp,amp)#两列泛音强度的格点（方便两两计算）
    return np.sum(disSin(s1,s2,amp1,amp2))#将所有不协和度相加得到总不协和度


def disTone2(hz1,hz2):#计算两音的不协和度
    harm = np.arange(1,512+1)
    harm1 = hz1*harm#第一个音的泛音列
    harm2 = hz2*harm#第二个音的泛音列
    harmTotal = np.append(harm1,harm2)
    amp = np.append(harm,harm)**-1.0#强度为调和级数递减
    s1,s2 = np.meshgrid(harmTotal,harmTotal)#两列泛音的格点（方便两两计算）
    amp1,amp2 = np.meshgrid(amp,amp)#两列泛音强度的格点（方便两两计算）
    return np.sum(disSin2(s1,s2,amp1,amp2))#将所有不协和度相加得到总不协和度

disRes = np.vectorize(disTone)(basicHz,HzRange)#计算指定频率范围相较基频的不协和度
plt.figure(dpi=512)
plt.plot(HzRange,disRes,linewidth=0.2)#绘图
plt.show()
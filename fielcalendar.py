# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 01:20:35 2024

@author: frank
"""
import numpy as np
import time
import datetime
def day2year(day):
    cycles = [(128,46751),(4,1461),(1,365)]
    year,s = 0,float('inf')
    for y,d in cycles:
        c = np.floor(day/d)
        year = year+y*c
        day = day-d*c
        if y*c==s:
            year=year-y
            day=day+d
            s = y
    return int(year),day

def day2mon(day):
    mon = (day+0.5)//30.5
    day = day-np.floor(mon*30.5)
    return int(mon+1),int(day+1)

class fieltime:
    def fieltime(self,sec):
        sec = sec-4*3600+719162*86400
        day = sec//86400
        year,day = day2year(day)
        year -= 1852
        mon,day = day2mon(day)
        sec=sec%86400
        #return (year,mon,day)+tuple(datetime.timedelta(seconds = sec))
        return f'菲历{year}年{mon}月{day}日 '\
            +str(datetime.timedelta(seconds = sec))
    def fielnow(self):
        text = self.fieltime(time.time())
        return text
    def earth2fiel(self,*date):
        earth = datetime.datetime(*date)
        return self.fieltime(earth.timestamp())
    #def showtime(sec):
        #t = fieltime(sec)
        #year,mon,day,sec=t[:3],t[3:]
        #return f'菲历{year}年{mon}月{day}日 '+str
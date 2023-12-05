# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:38:54 2023

@author: frank
"""

import numpy as np
from sympy import *

tone = ['F','C','G','D','A','E','B','F#','C#','G#','D#','A#']
pitch = []
mtf = 1/5**(1/4)

for i in range(7):
    
    i -= 0
    f = i % 4
    p = Rational(4,5)**(i//4) * (Rational(2,3)**f)*Rational(320+f,320)#tempered fifth
    p = p*2**floor(log(p,1/2)) #in an octave
    #pm = mtf**i
    #pm = pm*2**int(log(pm,1/2))
    pitch.append(p)
    name = tone[i] if i<12 else i
    print(name,float(p*1080))
#for i in range(30):
    #fifth = pitch[i]/pitch[i+1]
    #if fifth<1:fifth *= 2
    #print(float(fifth))
    
spitch = sorted(pitch+[Rational(1,2)])
steps = []
for i in range(7):
    step = spitch[(i+1)%31]/spitch[i]
    step = float(log(step,2)*1200)
    step = step % 1200
    #print(step)
    steps.append(step)
    #print(31-i,spitch[i])
    #print(('large ' if step>40 else 'small '),"%.2f" % step)
#print(sum(steps))
    
    
#for i in range(31):
    #if steps[i]>40:
        #print('large',end = ' ')
        #if steps[(i+1)%31]>40:print('\n')
    #else:print('small',end = ' ')
    
    
    #if step != Rational(128,125):
        #print(i,step,float(step))
#for i in range(31):
    #itv = pitch[(i+10)%31]/pitch[i]
    #if itv>1:itv/=2
    #diff = log(4/7,2) - log(itv,2)
    #diff *= 1200
    #print(i,float(diff))
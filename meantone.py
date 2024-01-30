# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:56:19 2023

@author: frank
"""

import numpy as np
from sympy import *
def cent(p):
    #print(p)
    return float(log(p,2)*1200)

chain = ['Db','Ab','Eb','Bb','F','C','G','D','A','E','B','F#',]
# chain of fifth

fif5 = 5**Rational(1,4) #5-limit meantone （5/4)
fif7 = 2*Rational(3,7)**Rational(1,3) #7-limit mentone (7/6)
fif7 = Rational(36,7)**Rational(1,4) #7-limit mentone (7/6)

print('5-limit meantone')
for i in range(12):
    pos = i-5
    p5 = fif5**pos
    p5 /= 2**floor(log(p5,2))
    print('%-5s%-25scent=%-10s' % (chain[i],p5,cent(p5)))
    
print('7-limit meantone')
for i in range(12):
    pos = i-5
    #p5 = fif5**pos
    #p5 /= 2**floor(log(p5,2))
    p7 = fif7**pos
    p7 /= 2**floor(log(p7,2))
    print('%-5s%-25scent=%-10s' % (chain[i],p7,cent(p7)))
    
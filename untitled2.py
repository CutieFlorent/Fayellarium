# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 07:53:50 2023

@author: frank
"""
import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt

P = 100
D = 100000

p_out = 0.1
O = int(P*p_out)
p_inf = 0.5
p_death = 0.0
d_inf = 15
d_rec = 10
rec_def = 1.0
lottery = 10

state = np.zeros(P,dtype=int)
state.fill(1)
days = np.zeros(P,dtype=int)
days.fill(0)
recs = np.zeros(P,dtype=int)
days.fill(0)
cases = np.zeros((D,4))


init_patients = rd.choice(range(P),10,replace=False)
for n in init_patients:
    state[n] = 2
#simulation
for i in range(D):
    n_out = rd.choice(range(P),int(O),replace=False)
    #print(len(n_out))
    patient = 0 
    for n in n_out:
        if state[n] == 2:patient += 1
    #print('patient',patient)
    rate = 1-(1-patient/O*p_inf)**lottery# 10 chances to infect
    #print('rate',rate)
    
    for n in n_out: #infect people
        if rd.uniform() < rate*rec_def**recs[n] and state[n] == 1:
            #rate*rec_def**recs[n] rate add rec deficits.
            #print('infect')
            state[n] = 2
            days[n] = 0
            
    cased = [0,0,0,0]
    for n in range(P): #update state
        if state[n] == 2 and days[n] > d_inf:
            if rd.uniform() < p_death*rec_def**-recs[n]:
                #p_death*rec_def**-recs[n] rec deficits increase death rate.
                state[n] = 0
            else:state[n] = 3
            days[n] = 0
        if state[n] == 3 and days[n] > d_rec:
            recs[n] += 1
            state[n] = 1
            days[n] = 0
        cased[state[n]]+=1
    cases[i] = cased
    days += 1
    if i % 100 == 0:print(i,cased)
#plot
x = list(range(D))
plt.plot(x, cases[:,1], color='blue', linestyle='-', label='healthy')
plt.plot(x, cases[:,2], color='red', linestyle='-', label='infected')
plt.plot(x, cases[:,3], color='green', linestyle='-', label='recovered')
plt.plot(x, cases[:,0], color='black', linestyle='-', label='dead')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Population of each state')
plt.legend()

plt.show()
    


        
        
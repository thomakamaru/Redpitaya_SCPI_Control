#!192.168.158.88
# -*- coding: utf-8 -*-
"""
@date: 06.09.2019
@author: Thomas Linde (jan_thomas.linde@tu-dresden.de)
Requirements : redpitaya_scpi
(API for the RP)
https://github.com/RedPitaya/RedPitaya/blob/master/Examples/python/redpitaya_scpi.py)

Device: Redpitaya STEMlab 14bit

"""
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import time
import pandas as pd
import os
import sys

plt.close('all')    #close all open plots

try:
    rp_s = scpi.scpi('192.168.158.88')  #IP of redpitaya - IS THE SCPI SERVER RUNNING?
    print('Connected to RedPitaya')
except:
    print('Redpitaya connection NOT successful.')
    print('Redpitaya running? SCPI Server running?.')
    sys.exit('Execution aborted')

#Prep the device. Reset. Acquire buffer size
rp_s.tx_txt('ACQ:RST')
rp_s.tx_txt('ACQ:BUF:SIZE?')
BUFF_SIZE = int(rp_s.rx_txt())
print(BUFF_SIZE)

avg_corr = -0.0215   #Average correction offset - the RP output channel seem to have some offset

""" Waveform input. Can be calculated manually (function). In this case a csv is read. """
#Locate the file with ~16000 values (csv) - Backslash must be forward slash!
my_file = '//----/Home-MA/Linde/09_Python-Projects/RP_Burst/vector.csv'

if os.path.isfile(my_file) : #check if file exists, else skip
    print('File Found!')
    data = pd.read_csv(my_file,delimiter=';',decimal=',',header=None).to_dict(orient='list')
else:
    print('File not found - check filepath and try again')

#convert interesting values to a list of floats
vek = list(float(i) for i in data[1])
#the redpitaya only takes string vectors!! this creates an empty one
y1=''

#go through the vector with the values and write each of the values into string for the RP
for i in range(0, len(vek)):
    if(i != len(vek)-1): 
        y1 +=  str(format((vek[i]), '.5f')) +', ' #dont forget to split by comma
    else:
        y1 += str(format((vek[i]), '.5f'))  #but no comma after the last value!
fn = [float(i) for i in y1.split(',')]      #just for checking the created string vector
rp_s.tx_txt('GEN:RST')                      #resets the RP
time.sleep(1)                               #wait in case something is still calculating

print('Function created')
#
rp_s.tx_txt('SOUR1:FUNC ARBITRARY')         #we do want to have our function
rp_s.tx_txt('SOUR1:TRAC:DATA:DATA '+y1)     #we pass over our own created string vector function
rp_s.tx_txt('SOUR1:VOLT 0.8')               #amplitude 
rp_s.tx_txt('SOUR1:VOLT:OFFS '+str(avg_corr)) #average correction
rp_s.tx_txt('SOUR1:FREQ:FIX 1')             #frequency 
rp_s.tx_txt('SOUR1:BURS:NCYC 1')            #how many burst cycles?
rp_s.tx_txt('OUTPUT1:STATE ON')             #output on
rp_s.tx_txt('SOUR1:BURS:STAT ON')           #burst on
rp_s.tx_txt('SOUR1:TRIG:SOUR EXT_PE')       #dont know what this does
print('Output ON')

while 1:
    rp_s.tx_txt('ACQ:TRIG:STAT?')
    if rp_s.rx_txt() == 'TD':
        break



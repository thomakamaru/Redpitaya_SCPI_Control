#!192.168.158.88

import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import numpy as np
import time
import math
plt.close('all')
rp_s = scpi.scpi('192.168.158.88')
print('Connected to RedPitaya')
rp_s.tx_txt('GEN:RST')
rp_s.tx_txt('ACQ:RST')
rp_s.tx_txt('ACQ:BUF:SIZE?')
BUFF_SIZE = int(rp_s.rx_txt())
#BUFF_SIZE = 15644
print(BUFF_SIZE)
f=50
y1=''
t=[]

#set up the values of the waveform
u50 = 1
f50 = 1
uharm = 0.1
fharm = 5

#calculate total waveform to normalize later
x  = np.linspace(0, 2*np.pi, BUFF_SIZE) # generates x axis in range 0 to 6 with 20000 points
y = u50*np.sin(2*np.pi*x)+uharm*np.sin(2*fharm*np.pi*x)
y_pk =float(np.std(y))

#for i in range(0, BUFF_SIZE):
#	t.append((2 * math.pi) / BUFF_SIZE * i)
t=list(np.linspace(0,2*np.pi,BUFF_SIZE))
for i in range(0, BUFF_SIZE-1):
    if(i != BUFF_SIZE-2): 
        val = (u50*math.sin(2*np.pi*t[i])+uharm* math.sin(2*fharm*np.pi*t[i]))*y_pk
        y1 += str(val)+ ', '
    else:
        val = (u50*math.sin(2*np.pi*t[i])+uharm* math.sin(2*fharm*np.pi*t[i]))*y_pk
        y1 += str(val)
fn = [float(i) for i in y1.split(',')]
#plt.plot(fn)
#x = x[]
print('Function created')
rp_s.tx_txt('SOUR1:FUNC ARBITRARY')
rp_s.tx_txt('SOUR1:TRAC:DATA:DATA '+y1)
rp_s.tx_txt('SOUR1:VOLT 1')
rp_s.tx_txt('SOUR1:FREQ:FIX 50')
rp_s.tx_txt('OUTPUT1:STATE ON')
print('Output ON')
time.sleep(1)



##Set Acquire
#rp_s.tx_txt('ACQ:DEC 64')
#rp_s.tx_txt('ACQ:TRIG:LEV 0')
#rp_s.tx_txt('ACQ:TRIG:DLY 0')
#
##Start gen % acq
#rp_s.tx_txt('ACQ:START')
#time.sleep(1)
#rp_s.tx_txt('ACQ:TRIG AWG_PE')
#rp_s.tx_txt('SOUR1:TRIG:IMM')           #Set generator trigger to immediately

#Wait for trigger
while 1:
    rp_s.tx_txt('ACQ:TRIG:STAT?')
    if rp_s.rx_txt() == 'TD':
        break

rp_s.tx_txt('SOUR1:TRAC:DATA:DATA?')
buff_string = rp_s.rx_txt()
buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
buff = list(map(float, buff_string))

#rp_s.tx_txt('ACQ:SOUR1:DATA?')
#meas_string = rp_s.rx_txt()
#meas_string = meas_string.strip('{}\n\r').replace("  ", "").split(',')
#meas = list(map(float, meas_string))
#
##plt.plot(buff)
#plt.plot(meas)
##plt.plot(gen_out)
#plt.ylabel('Voltage')
#plt.show()

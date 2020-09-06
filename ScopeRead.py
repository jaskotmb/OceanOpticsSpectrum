import visa
import numpy as np
import matplotlib.pyplot as plt
import pyfirmata
import time
import os
import sys
import datetime
import csv
sys.path.append('C:\\Users\\Jerry\\IdeaProjects\\OLED_Tools')
import OLEDTools

os.chdir("C:\\Users\\Jerry\\Documents\\TRPL_Data")


# setup arduino
ard = pyfirmata.Arduino('COM4')

# setup oscilloscope
rm = visa.ResourceManager()
scope = rm.open_resource(rm.list_resources()[0])
scope.timeout = 10000
horScale = 100e-9 # horizontal scale in sec/div
vertScale = 2 # vertical scale in V/div
plotMin = -0.2e-6
plotMax = 1e-6
sampleName = input("Enter sample name: ")
pulseMax = int(input("Enter number of pulses to average: "))

print(scope.query('*IDN?'),end='')
scope.write("DAT:SOU CH1")
scope.write('ACQ:MOD:SAM')
scope.write('ACQ:STOPA SEQ')
print("Acquire mode: {}".format(scope.query('ACQ:MOD?')),end='')
# Set scales
scope.write('HOR:SCA {}'.format(horScale))
scope.write('CH1:SCA {}'.format(vertScale))
recLength = int(format(scope.query('WFMO:RECO?')))
print("Data points recording: {}".format(recLength))

scope.write('ACQ:STATE ON')

# get scaling factors
tscale = float(scope.query('wfmoutpre:xincr?'))
tstart = float(scope.query('wfmoutpre:xzero?'))
total_time = tscale * recLength
tstep = total_time/recLength
tstop = tstart + total_time
scaled_time = np.linspace(tstart, tstop, num=recLength, endpoint=False)
vscale = float(scope.query('wfmoutpre:ymult?')) # volts / level
voff = float(scope.query('wfmoutpre:yzero?')) # reference voltage
vpos = float(scope.query('wfmoutpre:yoff?')) # reference position (level)
# Create a directory for saving TRPL data
if not os.path.exists(sampleName):
    os.mkdir(sampleName)
    print("Created Directory for sample: {}\\{}".format(os.getcwd(),sampleName))
os.chdir(sampleName)
print("Changed Directory to: {}".format(os.getcwd()))

# begin triggering with arduino
pulse = 0
dataList = []
skip = 0
# Loop to collect data from scope
while pulse < pulseMax:
    if(skip!='q'):
        skip = input("Press Enter to fire pulse, 'q' to run continuously")
    print("pulse #{}/{}, {:.2f}%".format(pulse+1,pulseMax,100*(pulse+1)/(pulseMax)))
    scope.write('ACQ:STATE ON')
    time.sleep(1)
    ard.digital[4].write(1)
    time.sleep(.5)
    ard.digital[4].write(0)
    temp = scope.query_binary_values('curve?', datatype='b', container=np.array)
    saveFn = '{}_{}of{}_{}.csv'.format(sampleName,(pulse+1),pulseMax,datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    headerTemp='Sample: {}, Pulse: {}/{}, Time: {}, Total Pts: {}, Scale: {} sec/step'.format(sampleName,(pulse+1),pulseMax,datetime.datetime.now(),recLength,tstep)
    scaledTemp = OLEDTools.formatTRPL(temp,vpos,vscale,voff)
    OLEDTools.npArrayWriteCsv(saveFn,scaled_time,scaledTemp,headerTemp)
    dataList.append(temp)
    pulse = pulse + 1
    time.sleep(0.5)

bin_wave = dataList[0]

# error checking
print('\nError Messages:')
r = int(scope.query('*esr?'))
print('event status register: 0b{:08b}'.format(r))
r = scope.query('allev?').strip()
print('all event messages: {}'.format(r))

scaledWaves = []
for i in range(len(dataList)):
    scaledWaves.append(OLEDTools.formatTRPL(dataList[i],vpos,vscale,voff))

# average all curves together

totalArray = scaledWaves[0]
if len(scaledWaves)>1:
    for i in range(1,len(scaledWaves)):
        totalArray = totalArray + scaledWaves[i]
totalArray = totalArray / len(scaledWaves)


hdr = 'Time (s)','Volts (V)','Sample: {}, Pulse: {}/{}, Time: {}, Total Pts: {}, Scale: {} sec/step'\
    .format('{}.csv'.format(sampleName),(pulse+1),pulseMax,datetime.datetime.now(),recLength,tstep)
OLEDTools.npArrayWriteCsv('{}-{}avg_{}.csv'.format(sampleName,pulseMax,datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')),scaled_time,totalArray,hdr)

# plotting
plt.semilogy(scaled_time, totalArray)
#plt.plot(scaled_time, totalArray)
plt.title('channel 1') # plot label
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.xlabel('time (seconds)') # x label
plt.ylabel('voltage (volts)') # y label
plt.xlim(plotMin, plotMax)
print("look for plot window...")
plt.show()

scope.close()


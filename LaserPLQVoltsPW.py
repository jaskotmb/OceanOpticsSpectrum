import visa
import os
import time
import glob
import sys
import numpy as np
sys.path.append('C:\\Users\\Jerry\\IdeaProjects\\OLED_Tools')
import OLEDTools
import csv

flag = 0
fName = "200823M36Vpbr"
sleepTime = 10
flag = 0
minVoltsPW = 1
maxVoltsPW = 20
totalPtsPW = int(((maxVoltsPW-minVoltsPW)*4)+1)
singleList = list(np.linspace(minVoltsPW,maxVoltsPW,totalPtsPW))

for xnum in range(1,2):
    if xnum >= 2:
        time.sleep(6)
        #time.sleep((sleepTime+11)*4*(18-maxVoltsPW)) # equalize total laser exposure time for runs that go up to less than 18V
    outListTotal = []
    for j in range(1,2):
        rm = visa.ResourceManager()
        B2901A = rm.list_resources()[0]
        smu = rm.open_resource(B2901A)

        smu.timeout = 5000000
        smu.write("*RST")
        print("SMU: {}".format(smu.query("*IDN?")))

        currList = []
        zeroLength = 4
        pulseLength = 4
        multiples = 1
        #vLevs = list(np.linspace(0+j*0.25,maxVolts,6))
        vLevs = list(np.linspace(0.25,minVoltsPW,4*minVoltsPW))
        vLevs.reverse()
        #vLevs = [-x for x in vLevs]
        voltList = []
        for i in range(len(vLevs)):
            voltList = voltList + ([0]*zeroLength + [vLevs[i]]*pulseLength)*multiples
        pulseTime = .01
        voltList = voltList + [0]*zeroLength
        voltList.reverse() # Reverse List
        print("Length of list: {}".format(len(voltList)))

        trigWidth = 5e-3 # range allowed is 1e-5 to 1e-2 seconds (.01 to 10 ms)
        listString = ','.join(str(x) for x in voltList)

        tbegin = time.time()
        print("Time Begin: {}".format(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(tbegin))))

        smu.write("*RST")
        smu.write(":SOUR:FUNC:MODE VOLT")
        smu.write(":SOUR:VOLT:RANG 200") # set in uA range (0.001)
        smu.write(":SOUR:VOLT:MODE LIST")
        smu.write(":SOUR:LIST:VOLT {}".format(listString))
        smu.write(':SENS:FUNC ""CURR""')
        smu.write(':SENS:CURR:RANG:AUTO ON')
        smu.write(':SENS:CURR:APER .02')
        smu.write(':SENS:CURR:PROT .04')
        smu.write(':FORM:DATA ASC')
        smu.write(':TRIG:SOUR AINT')
        smu.write(':TRIG:TIM {}'.format(pulseTime))
        smu.write(':TRIG:COUN {}'.format(len(voltList)))
        smu.write(":TRIG:MEAS:DEL .001")
        smu.write(':OUTP ON')
        smu.write(":SOUR:TOUT:STAT ON")
        smu.write(":SOUR:TOUT:SIGN EXT3")
        smu.write(":SOUR:DIG:EXT3:FUNC DIO")
        smu.write(":SOUR:DIG:EXT3:TOUT:EDGE:POS AFT") # set GPIO output trigger to after arm, trig, device actions
        smu.write(":SOUR:DIG:EXT3:TOUT:EDGE:WIDT {}".format(trigWidth))
        # Sets trigger width, in this case I am using the falling edge to trigger the spectrometer, so
        # this is effectively the delay between the current sourcing and spectrometer measurement
        # range allowed is 1e-5 to 1e-2 seconds (.01 to 10 ms)
        smu.write(':INIT (@1)')
        sourceVolt = smu.query(':FETC:ARR:VOLT? (@1)').split(',')
        measCurr = smu.query(':FETC:ARR:CURR? (@1)').split(',')
        smu.write(':OUTP OFF')

        tend = time.time()
        print("Time End: {}".format(tend))

        # Find all spectrum output files created in the time window of this script running
        oceanDir = 'C:\\Users\\Jerry\\oceanview'
        os.chdir(oceanDir)
        spectrumFileList = []
        for file in glob.glob("*.txt"):
            creationTime = os.path.getctime(file)
            if(creationTime > tbegin) and (creationTime < tend):
                print(file)
                spectrumFileList.append(file)

        # Open an Ocean Optics spectrum file, read its contents and return a list [wavelength, intensity]
        intAvg = []
        for i in range(len(spectrumFileList)):
            specList = OLEDTools.getSpectrum(spectrumFileList[i])
            wvl = list(zip(*specList))[0]
            intens = list(zip(*specList))[1]
            if flag == 0:
                initSpectrum = list(zip(wvl,intens))
                with open(fName+'_PL_initial.csv','w',newline='') as outfile:
                    wr = csv.writer(outfile)
                    wr.writerows(initSpectrum)
                flag = 1
            intAvg.append(OLEDTools.integrateSpectrum(wvl,intens,480,680)[0])
        for i in range(len(spectrumFileList)): # remove temporary spectrum files generated
            os.remove(spectrumFileList[i])
        currVoltTupIntens = list(zip(measCurr,sourceVolt,intAvg))
        outListTotal = outListTotal + currVoltTupIntens[0:-zeroLength]

        for j in range(1,totalPtsPW+1):
            time.sleep(sleepTime)
            rm = visa.ResourceManager()
            B2901A = rm.list_resources()[0]
            smu = rm.open_resource(B2901A)

            smu.timeout = 5000000
            smu.write("*RST")
            print("SMU: {}".format(smu.query("*IDN?")))

            currList = []
            zeroLength = 4
            pulseLength = 4
            multiples = 1
            vLevs = singleList[j-1]
            #vLevs = list(np.linspace(0+j*0.25,maxVolts,6))
            #vLevs = list(np.linspace(0.25,maxVolts,2*maxVolts))
            #vLevs = list(np.linspace(11,12,3))
            #vLevs.reverse()
            #vLevs = [-x for x in vLevs]
            voltList = []
            voltList = voltList + ([0]*zeroLength + [vLevs]*pulseLength)*multiples
            pulseTime = .01
            voltList = voltList + [0]*zeroLength
            voltList.reverse() # Reverse List
            print("Length of list: {}".format(len(voltList)))

            trigWidth = 5e-3 # range allowed is 1e-5 to 1e-2 seconds (.01 to 10 ms)
            listString = ','.join(str(x) for x in voltList)

            tbegin = time.time()
            print("Time Begin: {}".format(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(tbegin))))

            smu.write("*RST")
            smu.write(":SOUR:FUNC:MODE VOLT")
            smu.write(":SOUR:VOLT:RANG 200") # set in uA range (0.001)
            smu.write(":SOUR:VOLT:MODE LIST")
            smu.write(":SOUR:LIST:VOLT {}".format(listString))
            smu.write(':SENS:FUNC ""CURR""')
            smu.write(':SENS:CURR:RANG:AUTO ON')
            smu.write(':SENS:CURR:APER .02')
            smu.write(':SENS:CURR:PROT .04')
            smu.write(':FORM:DATA ASC')
            smu.write(':TRIG:SOUR AINT')
            smu.write(':TRIG:TIM {}'.format(pulseTime))
            smu.write(':TRIG:COUN {}'.format(len(voltList)))
            smu.write(":TRIG:MEAS:DEL .001")
            smu.write(':OUTP ON')
            smu.write(":SOUR:TOUT:STAT ON")
            smu.write(":SOUR:TOUT:SIGN EXT3")
            smu.write(":SOUR:DIG:EXT3:FUNC DIO")
            smu.write(":SOUR:DIG:EXT3:TOUT:EDGE:POS AFT") # set GPIO output trigger to after arm, trig, device actions
            smu.write(":SOUR:DIG:EXT3:TOUT:EDGE:WIDT {}".format(trigWidth))
            # Sets trigger width, in this case I am using the falling edge to trigger the spectrometer, so
            # this is effectively the delay between the current sourcing and spectrometer measurement
            # range allowed is 1e-5 to 1e-2 seconds (.01 to 10 ms)
            smu.write(':INIT (@1)')
            sourceVolt = smu.query(':FETC:ARR:VOLT? (@1)').split(',')
            measCurr = smu.query(':FETC:ARR:CURR? (@1)').split(',')
            smu.write(':OUTP OFF')

            tend = time.time()
            print("Time End: {}".format(tend))

            # Find all spectrum output files created in the time window of this script running
            oceanDir = 'C:\\Users\\Jerry\\oceanview'
            os.chdir(oceanDir)
            spectrumFileList = []
            for file in glob.glob("*.txt"):
                creationTime = os.path.getctime(file)
                if(creationTime > tbegin) and (creationTime < tend):
                    print(file)
                    spectrumFileList.append(file)

            # Open an Ocean Optics spectrum file, read its contents and return a list [wavelength, intensity]
            intAvg = []
            for i in range(len(spectrumFileList)):
                specList = OLEDTools.getSpectrum(spectrumFileList[i])
                wvl = list(zip(*specList))[0]
                intens = list(zip(*specList))[1]
                if flag == 0:
                    initSpectrum = list(zip(wvl,intens))
                    with open(fName+'_PL_initial.csv','w',newline='') as outfile:
                        wr = csv.writer(outfile)
                        wr.writerows(initSpectrum)
                    flag = 1
                intAvg.append(OLEDTools.integrateSpectrum(wvl,intens,480,680)[0])
            for i in range(len(spectrumFileList)): # remove temporary spectrum files generated
                os.remove(spectrumFileList[i])
            currVoltTupIntens = list(zip(measCurr,sourceVolt,intAvg))
            print(singleList[j-1])
            outListTotal = outListTotal + currVoltTupIntens[0:-zeroLength]
            os.chdir("C:\\Users\\Jerry\\IdeaProjects\\OceanOpticsSpectrum")
            with open(fName+"_{}.csv".format(xnum),'w') as resultFile:
                wr = csv.writer(resultFile,lineterminator='\n')
                wr.writerows(outListTotal)
        os.chdir("C:\\Users\\Jerry\\IdeaProjects\\OceanOpticsSpectrum")
        with open(fName+"_{}.csv".format(xnum),'w') as resultFile:
            wr = csv.writer(resultFile,lineterminator='\n')
            wr.writerows(outListTotal)

            #import matplotlib.pyplot as plt
            #plt.plot(intAvg)
            #plt.show()

import visa
import os
import time
import glob
import sys
sys.path.append('C:\\Users\\Jerry\\IdeaProjects\\OLED_Tools')
import OLEDTools
import csv

fName = "190719M24Vfr"
flag = 0
for j in range(1,11):
    rm = visa.ResourceManager()
    B2901A = rm.list_resources()[0]
    smu = rm.open_resource(B2901A)

    smu.timeout = 5000000
    smu.write("*RST")
    print("SMU: {}".format(smu.query("*IDN?")))

    currList = []
    zeroLength = 10
    pulseLength = 3
    multiples = 3
    vLevs = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,
             10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
    #vLevs.reverse()
    #vLevs = [-x for x in vLevs]
    voltList = []
    for i in range(len(vLevs)):
        voltList = voltList + ([0]*zeroLength + [vLevs[i]]*pulseLength)*multiples
    pulseTime = .025
    voltList = voltList + [0]*zeroLength
    voltList.reverse() # Reverse List
    print("Length of list: {}".format(len(voltList)))

    trigWidth = 5e-3 # range allowed is 1e-5 to 1e-2 seconds (.01 to 10 ms)
    listString = ','.join(str(x) for x in voltList)

    tbegin = time.time()
    print("Time Begin: {}".format(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(tbegin))))

    smu.write("*RST")
    smu.write(":SOUR:FUNC:MODE VOLT")
    smu.write(":SOUR:VOLT:RANG 20") # set in uA range (0.001)
    smu.write(":SOUR:VOLT:MODE LIST")
    smu.write(":SOUR:LIST:VOLT {}".format(listString))
    smu.write(':SENS:FUNC ""CURR""')
    smu.write(':SENS:CURR:RANG:AUTO ON')
    smu.write(':SENS:CURR:APER .15')
    smu.write(':SENS:CURR:PROT .005')
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
    os.chdir("C:\\Users\\Jerry\\IdeaProjects\\OceanOpticsSpectrum")
    with open(fName+"_{}.csv".format(j),'w') as resultFile:
        wr = csv.writer(resultFile,lineterminator='\n')
        wr.writerows(currVoltTupIntens)

    #import matplotlib.pyplot as plt
    #plt.plot(intAvg)
    #plt.show()

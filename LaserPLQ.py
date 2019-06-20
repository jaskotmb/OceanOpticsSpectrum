import visa
import os
import time
import glob
import sys
sys.path.append('C:\\Users\\jasko\\IdeaProjects\\OLED_Tools')
import OLEDTools
import csv

for j in range(1,6):
    rm = visa.ResourceManager()
    B2901A = rm.list_resources()[0]
    smu = rm.open_resource(B2901A)

    smu.timeout = 5000000
    smu.write("*RST")
    print("SMU: {}".format(smu.query("*IDN?")))

    currList = []
    zeroLength = 20
    pulseLength = 3
    multiples = 3
    uLevs = [1,2,3,4,5,6,7,8,9,10,15,20,30,40,50,60,70,80,90]
    uLevs = [x*1e-6 for x in uLevs]
    mLevs = [0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    mLevs = [x*1e-3 for x in mLevs]
    lev = uLevs + mLevs
    #lev = [-x for x in lev]
    currList = []
    for i in range(len(lev)):
        currList = currList + ([0]*zeroLength + [lev[i]]*pulseLength)*multiples
    pulseTime = .025
    currList = currList + [0]*zeroLength
    currList.reverse() # Reverse List
    print("Length of list: {}".format(len(currList)))

    trigWidth = 5e-3 # range allowed is 1e-5 to 1e-2 seconds (.01 to 10 ms)
    listString = ','.join(str(x) for x in currList)

    tbegin = time.time()
    print("Time Begin: {}".format(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(tbegin))))

    smu.write("*RST")
    smu.write(":SOUR:FUNC:MODE CURR")
    smu.write(":SOUR:CURR:RANG .001") # set in uA range (0.001)
    smu.write(":SOUR:CURR:MODE LIST")
    smu.write(":SOUR:LIST:CURR {}".format(listString))
    smu.write(':SENS:FUNC ""VOLT""')
    smu.write(':SENS:VOLT:RANG:AUTO ON')
    smu.write(':SENS:VOLT:APER .15')
    smu.write(':SENS:VOLT:PROT 20')
    smu.write(':FORM:DATA ASC')
    smu.write(':TRIG:SOUR AINT')
    smu.write(':TRIG:TIM {}'.format(pulseTime))
    smu.write(':TRIG:COUN {}'.format(len(currList)))
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
    sourceCurr = smu.query(':FETC:ARR:CURR? (@1)').split(',')
    measVolts = smu.query(':FETC:ARR:VOLT? (@1)').split(',')
    smu.write(':OUTP OFF')

    tend = time.time()
    print("Time End: {}".format(tend))

    # Find all spectrum output files created in the time window of this script running
    oceanDir = 'C:\\Users\\jasko\\oceanview'
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
        intAvg.append(OLEDTools.integrateSpectrum(wvl,intens,480,680)[0])
    for i in range(len(spectrumFileList)): # remove temporary spectrum files generated
        os.remove(spectrumFileList[i])
    currTupIntens = list(zip(currList,intAvg))
    os.chdir("C:\\Users\\jasko\\IdeaProjects\\OceanOpticsSpectrum")
    with open("190613M14_{}.csv".format(j),'w') as resultFile:
        wr = csv.writer(resultFile)
        wr.writerows(currTupIntens)

    #import matplotlib.pyplot as plt
    #plt.plot(intAvg)
    #plt.show()

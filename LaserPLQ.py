import visa
import os
import time
import glob
import sys
sys.path.append('C:\\Users\\Morty\\IdeaProjects\\OLED_Tools')
import OLEDTools

rm = visa.ResourceManager()
B2901A = rm.list_resources()[0]
smu = rm.open_resource(B2901A)

smu.timeout = 5000000
smu.write("*RST")
print("SMU: {}".format(smu.query("*IDN?")))

currList = [1e-3,2e-3,3e-3,4e-3,5e-3,6e-3,7e-3,8e-3]
pulseTime = 50e-3
trigWidth = 1e-2 # range allowed is 1e-5 to 1e-2 seconds (.01 to 10 ms)
listString = ','.join(str(x) for x in currList)

tbegin = time.time()
print("Time Begin: {}".format(tbegin))

smu.write("*RST")
smu.write(":SOUR:FUNC:MODE CURR")
smu.write(":SOUR:CURR:RANG 0.1")
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
oceanDir = 'C:\\Users\\Morty\\oceanview'
os.chdir(oceanDir)
spectrumFileList = []
for file in glob.glob("*.txt"):
    creationTime = os.path.getctime(file)
    if(creationTime > tbegin) and (creationTime < tend):
        print(file)
        spectrumFileList.append(file)

# Open an Ocean Optics spectrum file, read its contents and return a list [wavelength, intensity]
fn = 'C:\\Users\\Morty\\oceanview\\foo_HDX004611_00097.txt'

specList = OLEDTools.getSpectrum(fn)
wvl = list(zip(*specList))[0]
intens = list(zip(*specList))[1]


intAvg = OLEDTools.integrateSpectrum(wvl,intens,500,600)[0]
print(intAvg)

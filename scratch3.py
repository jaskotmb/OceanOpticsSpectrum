import visa
import numpy as np

rm = visa.ResourceManager()
scope = rm.open_resource(rm.list_resources()[0])
scope.timeout=10000

print(scope.query('*IDN?'))
scope.write("DAT:SOU CH1")
#scope.write('HEAD OFF')
print(scope.query("DAT:COMP:AVAIL?"))
#print(scope.query("HOR:RECO?"))
#scope.write('DATA:COMPOSITIONCOMPOSITE_YT')
#scope.write("DAT:WIDTH 1")
#scope.write("DAT:ENC ASCII")
#print(scope.query("CURVE?"))
#scope.write('CH1:IMP 50')
print(scope.query('CH1:IMP?'))
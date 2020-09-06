import pyfirmata
import time

board = pyfirmata.Arduino('COM4')
x=0
while True:
    input("Press Enter: ")
    print(x)
    x=x+1
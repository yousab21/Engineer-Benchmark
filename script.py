import serial
import time

PORT = '/dev/ttyUSB0'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=5)
time.sleep(2)  # wait for Arduino to finish resetting
def readNextLine():
    while(True):
        line = ser.readline().decode('utf-8').strip()
        if line:
            break
    return line

def forceTest():
    line = readNextLine()
    randomNumber = float(line)
    print(f"apply {randomNumber} newtons on the hook")
    line = readNextLine()
    error = float(line)
    print(f"you were off by {error} newtons")


while True:
    line = readNextLine()
    if line == 'StartForceTest':
        forceTest()
                

    


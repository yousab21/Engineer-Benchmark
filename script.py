import serial
import time

PORT = '/dev/ttyUSB0'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=5)
time.sleep(2)  # wait for Arduino to finish resetting

def readResponce():
    while(True):
        line = ser.readline().decode('utf-8').strip()
        if line:
            break
    return line

def sendRequest(request):
    ser.write(f'{request}\n'.encode())


def forceTest():
    sendRequest("FORCE_TEST")
    randomNumber = float(readResponce())
    print(f"apply {randomNumber} newtons on the hook")
    error = float(readResponce())
    print(f"you were off by {error}%")

def distanceTest():
    sendRequest("DISTANCE_TEST")
    randomNumber = float(readResponce())
    print(f"raise your hand {randomNumber}cm from the sensor")
    error = float(readResponce())
    print(f"you were off by {error}%")
                

    




import serial
import time

PORT = '/dev/ttyUSB0'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=5)
time.sleep(2)  # wait for Arduino to finish resetting

#=======================================
class Utils:
    def clear(self):
        print("\033[H\033[J", end="")
utils = Utils()
#========================================
class Ye_Old_Arduino_Handler:
    def __init__(self):
        return
    def readResponce(self):
        while(True):
            line = ser.readline().decode('utf-8').strip()
            if line:
                break
        return line

    def sendRequest(self, request):
        ser.write(f'{request}\n'.encode())

arduino = Ye_Old_Arduino_Handler()
#========================================

class Test:

    def __init__(self):
        self.keyWord = "UNKOWN"
        self.testName = "UNKOWN"
        self.instructions = "UNKOWN"
        self.timer = 0
        self.randomNumber = 0
        self.result = 0
        

    def getRandomNumber(self):
        self.randomNumber = float(arduino.readResponce())

    def getResult(self):
        self.result = float(arduino.readResponce())

    def printInstructions(self):
        utils.clear()
        print()
        print()
        print(f"------------------|| {self.testName}")
        print(f"------------------|| =============================")
        print(f"------------------|| instructions :")
        print(f"------------------|| {self.instructions} : [ {self.randomNumber} ]")
        time.sleep(3)
    
    def contdown(self):
        i = self.timer
        while(i > 0):
            utils.clear()
            print()
            print()
            print(f"              ==========")
            print(f"              ||      ||")
            print(f"              ||   {i}  ||")
            print(f"              ||      ||")
            print(f"              ========= ")
            i = i - 1
            time.sleep(1)

    def printResult(self):
        utils.clear()
        print()
        print()
        print(f"------------------|| result for {self.testName}")
        print(f"------------------|| =============================")
        print(f"------------------|| you were off by {self.result} %")
        print(f"------------------|| press enter to continue")
        input()

    def beginTest(self):
        arduino.sendRequest(self.keyWord)
        self.getRandomNumber()
        self.printInstructions()
        self.contdown()
        self.getResult()
        self.printResult()


class ForceTest(Test):
    keyWord = "FORCE_TEST"
    testName = "Force Perception Test"
    instructions = "apply the following number of newtons on the hook"
    timer = 5

class DistanceTest(Test):
    keyWord = "DISTANCE_TEST"
    testName = "Distance Perception Test"
    instructions = "Raise your hand the following number of cm above the sensor"
    timer = 5



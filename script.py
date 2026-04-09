

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
    def safeRead(self): #da 3shan bs lw msln el arduino 3ml disconnect fe 2y w2t, el readresponse htde None.
        response = self.readResponse() 
        while response is None:
            print("Waiting for Arduino...")
            time.sleep(2)
            response = self.readResponse()
        return float(response)
    
    def readResponse(self): #zwt bs error handling lw el arduino 3ml disconnect msh aktr
        try:
            while(True):
                line = ser.readline().decode('utf-8').strip()
                if line:
                   return line
        
        except serial.SerialException:
         print("Arduino disconnected!")
         return None
        
        except UnicodeDecodeError:
         print("Received bad data, retrying..")
         return self.readResponse()
    
    def sendRequest(self, request):
        ser.write(f'{request}\n'.encode())

arduino = Ye_Old_Arduino_Handler()
#========================================

class Test:

    keyWord = "UNKOWN"
    testName = "UNKOWN"
    instructions = "UNKOWN"
    timer = 0
    randomNumber = 0
    result = 0
    def __init__(self):
        pass
    def getRandomNumber(self):
        self.randomNumber = (arduino.safeRead())
    def getResult(self):
        self.result = (arduino.safeRead())

    def printInstructions(self):
        utils.clear()
        print()
        print()
        print(f"------------------|| {self.testName}")
        print(f"------------------|| =============================")
        print(f"------------------|| instructions :")
        print(f"------------------|| {self.instructions} : [ {self.randomNumber} ]")
        time.sleep(3)
    
    def countdown(self):
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
        self.countdown()
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

class ReflexTest(test):
    keyWord = "REFLEX_TEST"
    testName = "Reflex Test"
    instructions = "hold your hand above the sensor and remove it when you see the green light"
    timer = 8

#===============================================
class UI:
    def __init__(self):
        self.leaderboard = {}
    
    def welcomeScreen(self):
        utils.clear()
        print("\n ==== ENGINEER BENCHMARK ====")
    
    def getUsername(self):
        return input("Enter your name (or 'quit' to exit) : ")
    
    def showWelcomeBack(self, name, best_score):
        print(f"Welcome back {name}! Your best accuracy is {(best_score):.2f} % !")
    
    
    def showResults(self, name, avg, is_new_best):
        print(f"\n{name} your accuracy is {(avg):.2f}%")
        if is_new_best:
            print("New personal best!")
    
    
    def displayLeaderboard(self):
        if not self.leaderboard:
            print("\n ==== Leaderboard ====")
            print(" No scores yet.")
            #kan fi heda bas bug eno hydisplay el leadebaords for 10ms we yed5ol 3la el ba3do
            input("Press enter for new participant...")
            return
        sortedScores = sorted(self.leaderboard.items(), key=lambda x: x[1])
        print("\n ==== Leaderboard ====")
        for i, (name, score) in enumerate(sortedScores, 1):
           print(f"{i}, {name}: {(score):.2f}%")
        print("=============================")

    def updateLeaderboard(self, name, score):
        if name not in self.leaderboard or score < self.leaderboard[name]:
             self.leaderboard[name] = (score)
             return True
        return False



def main():
    ui = UI()
    while True:
        ui.welcomeScreen()
        name = ui.getUsername()

        if name.lower() == "quit":
            break
        if name in ui.leaderboard:
            ui.showWelcomeBack(name, ui.leaderboard[name])
        
        # running tests
        tests = [ForceTest() , DistanceTest() , ReflexTest() ] 
        errors = []
        for test in tests:
           test.beginTest()
           errors.append(test.result)
        avg = sum(errors)/len(errors)
        
        newBest = ui.updateLeaderboard(name, avg)
        ui.showResults(name, avg, newBest)
        ui.displayLeaderboard()
if __name__ == "__main__":
    main()

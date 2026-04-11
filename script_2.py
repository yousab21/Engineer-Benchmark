
import serial
import time
import json 
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

    def __init__(self):
        self.keyWord = "UNKOWN"
        self.testName = "UNKOWN"
        self.instructions = "UNKOWN"
        self.timer = 0
        self.randomNumber = 0
        self.result = 0

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
class ReflexTest(Test):
    keyWord = "REFLEX_TEST"
    testName = "Reflex Test"
    instructions = "hold your hand above the sensor and remove it when you see the green light"
    timer = 0 


    def countdown(self):
        utils.clear()
        print()
        print()
        print("waiting for you to finish the test")
        print()
        
    def printResult(self):
        utils.clear()
        print()
        print()
        print(f"------------------|| result for {self.testName}")
        print(f"------------------|| =============================")
        print(f"------------------|| your reflex is {self.result}ms")
        print(f"------------------|| press enter to continue")
        input()

#================================================

class JsonParcer():
    def __init__(self):
        self.filename = "scores.json"
        
    def loadScores(self): 
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
                return {}
        
    def saveScores(self,data): 
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=2)
            
parcer = JsonParcer()

#===============================================
class UI:
    def __init__(self): 
        self.leaderboard = parcer.loadScores()

    def welcomeScreen(self):
        utils.clear()
        print("\n ==== ENGINEER BENCHMARK ====")
    
    def getUsername(self):
        return input("Enter your name (or 'quit' to exit)")


    def showWelcomeBack(self,name, data):
        print(f"Welcome back {name}!, Your best results are below.")
        print(f"Force: {data['Station1(F)']:.2f}%")        
        print(f"Distance: {data['Station2(D)']:.2f}%")        
        print(f"Reaction: {data['Station3(R)']:.2f}ms")        
        print(f"AvgScore: {data['AverageScore']:.2f}%")        
 

    def showResults(self, name, errorsList, avg, isNewBest):
        print(f"\n{name}, your results for this session:")
        print(f"  Force: {errorsList[0]:.2f}%")
        print(f"  Distance: {errorsList[1]:.2f}%")
        print(f"  Reaction: {errorsList[2]:.2f}ms")
        print(f"  Average: {avg:.2f}%")
        if isNewBest:
             print("New personal best!")

    
    def displayLeaderboard(self):
        if not self.leaderboard:
            print("\n ==== Leaderboard ====")
            print(" No scores yet.")
            input("Press enter for new participant...")
            return
        sortedScores = sorted(self.leaderboard.items(), key=lambda x: x[1]["AverageScore"]) #el sort brdo bysht8l bel avgscore
        print("\n ==== Leaderboard ====")
        for i, (name, data) in enumerate(sortedScores, 1):
           print(f"{i}. {name}")
           print(f"   ┌───────────────────────────────────────┐") #el symbols de hna https://en.wikipedia.org/wiki/Box-drawing_characters
           print(f"   │ Force   │ Distance│ Reaction│ Average │")
           print(f"   ┣───────────────────────────────────────┤")
           print(f"   │ {data['Station1(F)']:7.2f} │ {data['Station2(D)']:7.2f} │ {data['Station3(R)']:7.2f} │ {data['AverageScore']:7.2f} │")
           print(f"   └───────────────────────────────────────┘")
                 

    def updateLeaderboard(self, name, errorsList, avgScore):
        if name not in self.leaderboard or avgScore < self.leaderboard[name]["AverageScore"]:
            self.leaderboard[name] = {
                "Station1(F)": errorsList[0],
                "Station2(D)": errorsList[1],
                "Station3(R)": errorsList[2],
                "AverageScore": avgScore
            }
            parcer.saveScores(self.leaderboard)
            return True
        return False
    
#==========================================

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
        tests = [ForceTest(), DistanceTest(),ReflexTest()]
        results = []
        for test in tests:
           test.beginTest()
           results.append(test.result)
        avg = (results[0]+results[1])/2 #hna ana shelt mwdo3 el len da 7alyn 3shan el reflextest asln msh error fna msh 3arf a3ml fe7 eh 7alyn 
        newBest = ui.updateLeaderboard(name,results, avg)
        ui.showResults(name,results, avg, newBest)
        ui.displayLeaderboard()

if __name__ == "__main__":
    main()
    

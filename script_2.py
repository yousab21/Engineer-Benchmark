import serial
import time
import json
import os
from colorama import Fore,Back, Style, init
init()
PORT = '/dev/ttyUSB0'
BAUD = 9600

#=======================================
class Utils:
    def clear(self):
        print("\033[H\033[J", end="")

    def print_centered(self, value, end="\n"):
        width = os.get_terminal_size().columns
        print(str(value).center(width), end=end)

utils = Utils()
#========================================
class Ye_Old_Arduino_Handler:
    def __init__(self, ser):
        self.ser = ser

    def safeRead(self):
        response = self.readResponse()
        while response is None:
            utils.print_centered("Waiting for Arduino...")
            time.sleep(2)
            response = self.readResponse()
        if "ERROR" in response:
            utils.print_centered(f"Sensor error: {response}")
            return 0.0
        return float(response)

    def readResponse(self):
        try:
            attempts = 0
            while attempts < 10:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    return line
                attempts += 1
            utils.print_centered("Timed out waiting for Arduino.")
            return None
        except serial.SerialException:
            utils.print_centered("Arduino disconnected!")
            return None
        except UnicodeDecodeError:
            utils.print_centered("Received bad data, retrying..")
            return self.readResponse()

    def sendRequest(self, request):
        self.ser.reset_input_buffer()
        self.ser.write(f'{request}\n'.encode())

#========================================
class Ye_Other_Json_Parcer():
    def __init__(self):
        self.filename = "scores.json"


    def loadScores(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def saveScores(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=2)
            
parcer = Ye_Other_Json_Parcer()
#=========================================
class Admin:
    def __init__(self, ui):
        self.adminPassword = "5G6E74"
        self.ui =ui
    def deleteEverything(self):
        parcer.saveScores({})

    
    def deleteUser(self,name):
        data = parcer.loadScores()
        if name in data:
            del data[name]
            parcer.saveScores(data)
            return True
        return False
    
    def verifyPassword(self):
        utils.print_centered("Enter password: ")
        password = input()
        if password != self.adminPassword:
            utils.print_centered("Invalid password, returning to menu.")
            return False
        return True

    def adminScreen(self):
        utils.clear()
        utils.print_centered(f"{Style.BRIGHT}{Back.WHITE}{Fore.RED}=== Admin Mode. ==={Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}{Fore.YELLOW}Enter a number..{Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}1.Delete a user{Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}2.Empty the leaderboard.{Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}3.Return to menu.{Style.RESET_ALL}")

        while True:
            adminAns = input()
            if(adminAns == "3"): break
            elif(adminAns == "2"):
                if not self.ui.leaderboard:
                    utils.print_centered("Leaderboard is already empty.")
                else:
                    self.deleteEverything()
                    self.ui.leaderboard = {}
                    utils.print_centered("Leaderboard cleared.")
            elif adminAns == "1":
                    utils.print_centered("Enter the name of the user:")
                    name = input()
                    if self.deleteUser(name.lower()):
                        del self.ui.leaderboard[name.lower()]
                        utils.print_centered(f"{name} deleted successfully.")
                    else:
                        utils.print_centered("User not found.")
#=======================================
class Test:
    def __init__(self, arduino):
        self.arduino = arduino
        self.randomNumber = 0
        self.result = 0
        try:
            self.keyWord = getattr(self.__class__, "keyWord")
            self.testName = getattr(self.__class__, "testName")
            self.instructions = getattr(self.__class__, "instructions")
            self.timer = getattr(self.__class__, "timer")
        except AttributeError as e:
            raise Exception(f"{self.__class__.__name__} is missing required attribute: {e}")
    def getRandomNumber(self):
        self.randomNumber = self.arduino.safeRead()

    def getResult(self):
        self.result = self.arduino.safeRead()

    def printInstructions(self):
        utils.clear()
        print()
        print()
        utils.print_centered(f"{self.testName}")
        utils.print_centered(f"=====================================")
        utils.print_centered(f"instructions :")
        utils.print_centered(f"{self.instructions} : [ {self.randomNumber} ]")
        time.sleep(3)

    def countdown(self):
        i = self.timer
        while i > 0:
            utils.clear()
            print()
            print()
            utils.print_centered(f"==========")
            utils.print_centered(f"||      ||")
            utils.print_centered(f"||   {i}  ||")
            utils.print_centered(f"||      ||")
            utils.print_centered(f"========= ")
            i -= 1
            time.sleep(1)

    def printResult(self):
        utils.clear()
        print()
        print()
        utils.print_centered(f"result for {self.testName}")
        utils.print_centered(f"=======================================")
        utils.print_centered(f"you were off by {self.result} %")
        utils.print_centered(f"press enter to continue")
        input()

    def beginTest(self):
        self.arduino.sendRequest(self.keyWord)
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

    def printResult(self):
        utils.clear()
        print()
        print()
        utils.print_centered(f"result for {self.testName}")
        utils.print_centered(f"=============================")
        utils.print_centered(f"your reflex is {self.result}ms")
        utils.print_centered(f"press enter to continue")
        input()

    def countdown(self):
        utils.clear()
        print()
        print()
        utils.print_centered("test running — FOCUS UP !")
        print()

class TimePerceptionTest(Test):
    keyWord = "TIME_TEST"
    testName = "Time Perception Test"
    instructions = "count the following number of seconds in your head then tap the sensor"
    timer = 3


class AnglePerceptionTest(Test):
    keyWord = "ANGLE_TEST"
    testName = "Angle Perception Test"
    instructions = "tilt the device to the following angle in degrees"
    timer = 5

    def printResult(self):
        utils.clear()
        print()
        print()
        utils.print_centered(f"result for {self.testName}")
        utils.print_centered(f"=======================================")
        utils.print_centered(f"you were off by {self.result} %")
        utils.print_centered(f"press enter to continue")
        input()

#===============================================
class UI:
    def __init__(self):
        self.leaderboard = parcer.loadScores()

    def welcomeScreen(self):
        utils.clear()
        utils.print_centered("=========== ENGINEER BENCHMARK =============")
        utils.print_centered("Enter a number.")
        utils.print_centered("1. Begin Trials")
        utils.print_centered("2. View Leaderboard")
        utils.print_centered("3. Enter Admin mode.")
        return input()
    
              
    
    def getUsername(self):
        utils.print_centered(f"Enter your name (or 'quit' to exit): ", end="")
        return input()

    def showWelcomeBack(self, name, data):
        utils.print_centered(f"Welcome back {name}!, Your best results are below.")
        utils.print_centered(f"Force:      {data['Station1(F)']:.2f}%")
        utils.print_centered(f"Distance:   {data['Station2(D)']:.2f}%")
        utils.print_centered(f"Reaction:   {data['Station3(R)']:.2f}ms")
        utils.print_centered(f"Time:       {data['Station4(T)']:.2f}%")
        utils.print_centered(f"Angle:      {data['Station5(A)']:.2f}%")
        utils.print_centered(f"AvgScore:   {data['AverageScore']:.2f}%")
        utils.print_centered(f"press enter to continue : ")
        input()

    def showResults(self, name, errorsList, avg, isNewBest):
        utils.print_centered(f"{name}, your results for this session:")
        utils.print_centered(f"Force:      {errorsList[0]:.2f}%")
        utils.print_centered(f"Distance:   {errorsList[1]:.2f}%")
        utils.print_centered(f"Reaction:   {errorsList[2]:.2f}ms")
        utils.print_centered(f"Time:       {errorsList[3]:.2f}%")
        utils.print_centered(f"Angle:      {errorsList[4]:.2f}%")
        utils.print_centered(f"Average:    {avg:.2f}%")
        if isNewBest:
            utils.print_centered("New personal best!")
        utils.print_centered(f"press enter to continue : ")
        input()

    def showLeaderboardHeader(self):
        header  = f"{'Name':<12} | {'Force%':>8} | {'Distance%':>9} | {'Reaction(ms)':>12} | {'Time%':>7} | {'Angle%':>7} | {'Average%':>8}"
        divider = "-" * len(header)
        utils.print_centered(header)
        utils.print_centered(divider)

    def displayLeaderboard(self):
        utils.print_centered("============ Leaderboard ==============")
        if not self.leaderboard:
            utils.print_centered("No scores yet.")
            utils.print_centered(f"Press enter for new participant...")
            input()
            return
        sortedScores = sorted(self.leaderboard.items(), key=lambda x: x[1]["AverageScore"])
        self.showLeaderboardHeader()
        for i, (name, data) in enumerate(sortedScores, 1):
            row = f"{f'{i}. {name.capitalize()}':<12} | {data['Station1(F)']:>8.2f} | {data['Station2(D)']:>9.2f} | {data['Station3(R)']:>12.2f} | {data['Station4(T)']:>7.2f} | {data['Station5(A)']:>7.2f} | {data['AverageScore']:>8.2f}"
            utils.print_centered(row)
        utils.print_centered(f"Press enter for new participant...")
        input()

    def updateLeaderboard(self, name, errorsList, avgScore):
        name = name.lower()
        if name not in self.leaderboard or avgScore < self.leaderboard[name]["AverageScore"]:
            self.leaderboard[name] = {
                "Station1(F)": errorsList[0],
                "Station2(D)": errorsList[1],
                "Station3(R)": errorsList[2],
                "Station4(T)": errorsList[3],
                "Station5(A)": errorsList[4],
                "AverageScore": avgScore
            }
            parcer.saveScores(self.leaderboard)
            return True
        return False

#==========================================
def main():
    print("Connecting to Arduino...")
    ser = serial.Serial(PORT, BAUD, timeout=5)
    time.sleep(10)
    ser.reset_input_buffer()
    print("Connected!")

    arduino = Ye_Old_Arduino_Handler(ser)
    ui = UI()
    admin = Admin(ui)

    try:
        while True:
            while True:
                ans = ui.welcomeScreen()
                if ans == "1":
                    break
                elif ans == "2": 
                    ui.displayLeaderboard()
                    utils.print_centered("Returning to menu...")
                    time.sleep(2)  
                elif ans == "3":
                    if admin.verifyPassword():
                       admin.adminScreen()
                else: utils.print_centered("Invalid input, Try again.")         

            while True:
                utils.clear()
                name = ui.getUsername()
                name = name.lower()
                if name == "quit": break
                if name.strip() != "": break
                utils.print_centered("Name cannot be empty. Try again.")
                time.sleep(2) 
            if name == "quit": break

            if name in ui.leaderboard:
                ui.showWelcomeBack(name.capitalize(), ui.leaderboard[name])

            tests = [ForceTest(arduino), DistanceTest(arduino), ReflexTest(arduino), TimePerceptionTest(arduino), AnglePerceptionTest(arduino)]
            results = []
            for test in tests:
                utils.print_centered("Test beginning in 5 seconds, Get Ready.")
                time.sleep(5)
                test.beginTest()
                results.append(test.result)

            avg = (results[0] + results[1] + results[3] + results[4]) / 4
            newBest = ui.updateLeaderboard(name, results, avg)
            ui.showResults(name.capitalize(), results, avg, newBest)
            ui.displayLeaderboard()
    finally:
        utils.clear()
        utils.print_centered("Exiting the ENGINEER BENCHMARK. Goodbye.")
        ser.close()

if __name__ == "__main__":
   main()



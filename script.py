
import serial
import time
import json
import os
import tempfile
from colorama import Fore, Back, Style, init
init()

#PORT = '/dev/ttyUSB0'
PORT = '/dev/ttyACM0'
BAUD = 9600

#=======================================
class Utils:
    def clear(self):
        print("\033[H\033[J", end="")

    def print_centered(self, value, end="\n"):
        width = os.get_terminal_size().columns
        print(str(value).center(width), end=end)

utils = Utils()

#=======================================
def reflexColor(score):
    if score < 200:   return Fore.GREEN
    elif score < 300: return Fore.YELLOW
    else:             return Fore.RED

def percentColor(score):
    if score >= 90:   return Fore.GREEN
    elif score >= 75: return Fore.YELLOW
    else:             return Fore.RED

# Order: Reflex, Force, Distance, Angle, Time
SCORE_COLORS = [reflexColor, percentColor, percentColor, percentColor, percentColor]

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
class Ye_Other_Json_Parcer:
    def __init__(self):
        self.filename = "scores.json"

    def loadScores(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def saveScores(self, data):
       while True:
            try:
                dir = os.path.dirname(os.path.abspath(self.filename))
                with tempfile.NamedTemporaryFile('w',dir=dir, delete=False, suffix='.tmp') as tmp:
                    json.dump(data,tmp,indent=2)
                    tmp_path=tmp.name
                os.replace(tmp_path, self.filename)
                break
            except OSError as error:
                utils.print_centered("Failed to save.. Retrying..")
                time.sleep(1)


parcer = Ye_Other_Json_Parcer()

#=========================================
class Admin:
    def __init__(self, ui):
        self.adminPassword = "AOOYY" #our initials (ahmad omar omar yehia yousab)
        self.ui = ui

    def deleteEverything(self):
        parcer.saveScores({})

    def deleteUser(self, name):
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
        utils.print_centered(f"{Style.BRIGHT}{Back.WHITE}{Fore.RED}=== Admin Mode ==={Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}{Fore.YELLOW}Enter a number..{Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}1. Delete a user{Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}2. Empty the leaderboard{Style.RESET_ALL}")
        utils.print_centered(f"{Back.GREEN}3. Return to menu{Style.RESET_ALL}")

        while True:
            adminAns = input()
            if adminAns == "3":
                break
            elif adminAns == "2":
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
                    self.ui.leaderboard.pop(name.lower(), None) #safer to delete this way
                    utils.print_centered(f"{name} deleted successfully.")
                else:
                    utils.print_centered("User not found.")

#=======================================
class Test:
    def __init__(self, arduino):
        self.arduino = arduino
        self.randomNumber = 0
        self.error = 0
        try:
            self.keyWord     = getattr(self.__class__, "keyWord")
            self.testName    = getattr(self.__class__, "testName")
            self.instructions = getattr(self.__class__, "instructions")
            self.timer       = getattr(self.__class__, "timer")
            self.goodScore       = getattr(self.__class__, "goodScore")
            self.okScore       = getattr(self.__class__, "okScore")
            self.badScore      = getattr(self.__class__, "badScore")
        except AttributeError as e:
            raise Exception(f"{self.__class__.__name__} is missing required attribute: {e}")

    def calculateScore(self):
        return max(0, 100 - self.error)

    def getRandomNumber(self):
        self.randomNumber = self.arduino.safeRead()

    def getResult(self):
        self.error = self.arduino.safeRead()

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

    def bullyParticipant(self):
        print()
        if (self.calculateScore() > 90):
            utils.print_centered(f"{Style.BRIGHT}{Fore.GREEN}{self.goodScore}{Style.RESET_ALL}")

        elif (self.calculateScore() > 75):
            utils.print_centered(f"{Style.BRIGHT}{Fore.YELLOW}{self.okScore}{Style.RESET_ALL}")

        else:
            utils.print_centered(f"{Style.BRIGHT}{Fore.RED}{self.badScore}{Style.RESET_ALL}")
        print()


    def printResult(self):
        accuracy = max(0, 100 - self.error)
        color = percentColor(accuracy)

        utils.clear()
        print()
        print()
        utils.print_centered(f"result for {self.testName}")
        utils.print_centered(f"=======================================")

        plainText = f"you were {accuracy}% correct"
        width = os.get_terminal_size().columns
        print(plainText.center(width).replace(str(accuracy), f"{Style.BRIGHT}{color}{accuracy}{Style.RESET_ALL}"))
        self.bullyParticipant()
        utils.print_centered(f"press enter to continue")
        input()

    def beginTest(self):
        self.arduino.sendRequest(self.keyWord)
        self.getRandomNumber()
        self.printInstructions()
        self.countdown()
        self.getResult()
        self.printResult()


class ReflexTest(Test):
    keyWord = "REFLEX_TEST"
    testName = "Reflex Test"
    instructions = "hold your hand above the sensor and remove it when you see the green light"
    timer = 0
    goodScore = "looks like we have a professional gamer on our hand !"
    okScore = "not too slow, not to fast, you hand are just... there"
    badScore = "have you had breakfast yet?, WAKE UP GRANDPA !"

    def calculateScore(self):
        return self.error

    def countdown(self):
        utils.clear()
        print()
        print()
        utils.print_centered("test running — FOCUS UP !")
        print()

    def bullyParticipant(self):
        print()
        if (self.calculateScore() < 200):
            utils.print_centered(f"{Style.BRIGHT}{Fore.GREEN}{self.goodScore}{Style.RESET_ALL}")

        elif (self.calculateScore() < 300):
            utils.print_centered(f"{Style.BRIGHT}{Fore.YELLOW}{self.okScore}{Style.RESET_ALL}")

        else:
            utils.print_centered(f"{Style.BRIGHT}{Fore.RED}{self.badScore}{Style.RESET_ALL}")
        print()


    def printResult(self):
        reflex = self.error
        color = reflexColor(reflex)

        utils.clear()
        print()
        print()
        utils.print_centered(f"result for {self.testName}")
        utils.print_centered(f"=======================================")

        plainText = f"your reaction time: {reflex}ms"
        width = os.get_terminal_size().columns
        print(plainText.center(width).replace(str(reflex), f"{Style.BRIGHT}{color}{reflex}{Style.RESET_ALL}"))
        self.bullyParticipant()
        utils.print_centered(f"press enter to continue")
        input()


class ForceTest(Test):
    keyWord = "FORCE_TEST"
    testName = "Force Perception Test"
    instructions = "apply the following number of newtons on the hook"
    timer = 5
    goodScore = "NASA-grade touch !"
    okScore = "the force you applied is... there"
    badScore = "Newton is lucky to be dead at this point"


class DistanceTest(Test):
    keyWord = "DISTANCE_TEST"
    testName = "Distance Perception Test"
    instructions = "Raise your hand the following number of cm above the sensor"
    timer = 5
    goodScore = "ISP-certified eyeballing"
    okScore = "that was as accurate as most of our prep year drawings tbh"
    badScore = "you fabricated a lot of drawing in prep year, didn't you?"


class AnglePerceptionTest(Test):
    keyWord = "ANGLE_TEST"
    testName = "Angle Perception Test"
    instructions = "tilt the device to the following angle in degrees"
    timer = 5
    goodScore = "cleaner than a CAD constraint !"
    okScore = "close enough, for a rough sketch"
    badScore = "radiands? degrees? well you chose neither !"


class TimePerceptionTest(Test):
    keyWord = "TIME_TEST"
    testName = "Time Perception Test"
    instructions = "count the following number of seconds in your head then tap the sensor"
    timer = 0
    goodScore = "atomic clock behavior !"
    okScore = "RealTime? more like sometimes"
    badScore = "bro lags as if he was on egyptian WIFI !"

    def countdown(self):
        utils.clear()
        print()
        print()
        utils.print_centered(f"{Fore.GREEN}timer started, KEEP FOCUS !{Style.RESET_ALL}")
        print()

#===============================================
class UI:
    def __init__(self):
        self.leaderboard = parcer.loadScores()

    def welcomeScreen(self):
        utils.clear()
        utils.print_centered(r"╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
        utils.print_centered(r"║   ______ _   _  _____ _____ _   _ ______ ______ _____        ____  ______ _   _  _____ _    _ __  __          _____  _  __  ║")
        utils.print_centered(r"║  |  ____| \ | |/ ____|_   _| \ | |  ____|  ____|  __ \      |  _ \|  ____| \ | |/ ____| |  | |  \/  |   /\   |  __ \| |/ /  ║")
        utils.print_centered(r"║  | |__  |  \| | |  __  | | |  \| | |__  | |__  | |__) |     | |_) | |__  |  \| | |    | |__| | \  / |  /  \  | |__) | ' /   ║")
        utils.print_centered(r"║  |  __| | . ` | | |_ | | | | . ` |  __| |  __| |  _  /      |  _ <|  __| | . ` | |    |  __  | |\/| | / /\ \ |  _  /|  <    ║")
        utils.print_centered(r"║  | |____| |\  | |__| |_| |_| |\  | |____| |____| | \ \      | |_) | |____| |\  | |____| |  | | |  | |/ ____ \| | \ \| . \   ║")
        utils.print_centered(r"║  |______|_| \_|\_____|_____|_| \_|______|______|_|  \_\     |____/|______|_| \_|\_____|_|  |_|_|  |_/_/    \_\_|  \_\_|\_\  ║")
        utils.print_centered(r"║                                                                                                                             ║")
        utils.print_centered(r"╚═════════════════════════════════════════════════════════ ▲ ═════════════════════════════════════════════════════════════════╝")
        utils.print_centered("")
        utils.print_centered("Enter a number.")
        utils.print_centered("1. Begin Trials")
        utils.print_centered("2. View Leaderboard")
        utils.print_centered("3. Enter Admin mode.")
        return input()

    def getUsername(self):
        utils.clear()
        utils.print_centered(f"Enter your name (or 'quit' to exit): ", end="")
        return input()

    def showWelcomeBack(self, name, data):
        utils.print_centered(f"Welcome back {name}! Your best results are below.")
        utils.print_centered(f"Reaction:   {data['Station1(R)']:.2f}ms")
        utils.print_centered(f"Force:      {data['Station2(F)']:.2f}%")
        utils.print_centered(f"Distance:   {data['Station3(D)']:.2f}%")
        utils.print_centered(f"Angle:      {data['Station4(A)']:.2f}%")
        utils.print_centered(f"Time:       {data['Station5(T)']:.2f}%")
        utils.print_centered(f"AvgScore:   {data['AverageScore']:.2f}%")
        utils.print_centered(f"press enter to continue : ")
        input()

    def showResults(self, name, scoresList, avg, isNewBest):
        utils.clear()
        utils.print_centered(f"{name}, your results for this session:")
        labels = ["Reaction:", "Force:   ", "Distance:", "Angle:   ", "Time:    "]
        units  = ["ms",        "%",         "%",         "%",         "%"        ]
        for i, (score, label, unit) in enumerate(zip(scoresList, labels, units)):
            color = SCORE_COLORS[i](score)
            plainText = f"{label}  {score:.2f}{unit}"
            width = os.get_terminal_size().columns
            scoreStr = f"{score:.2f}"
            print(plainText.center(width).replace(scoreStr, f"{Style.BRIGHT}{color}{scoreStr}{Style.RESET_ALL}"))
        utils.print_centered(f"Average:    {avg:.2f}%")
        if isNewBest:
            utils.print_centered("New personal best!")
            rank = sum(1 for person in self.leaderboard.values() if person["AverageScore"]>avg) +1
            total = len(self.leaderboard)
            utils.print_centered(f"You are now ranked {rank} out of {total}!")
        utils.print_centered(f"press enter to continue : ")
        input()

    def showLeaderboardHeader(self):
        header  = f"{'Name':<20} | {'Reaction(ms)':>12} | {'Force%':>12} | {'Distance%':>12} | {'Angle%':>12} | {'Time%':>12} | {'Average%':>12}"
        divider = "-" * len(header)
        utils.print_centered(header)
        utils.print_centered(divider)

    def displayLeaderboard(self):
        utils.clear()
        utils.print_centered(r"╔═══════════════════════════════════════════════════════════════════════════════════════════════╗")
        utils.print_centered(r"║   _      ______          _____  ______  _____     ____   ____          _____  _____   _____   ║")
        utils.print_centered(r"║  | |    |  ____|   /\   |  __ \|  ____||  __ \   |  _ \ / __ \   /\   |  __ \|  __ \ / ____   ║")
        utils.print_centered(r"║  | |    | |__     /  \  | |  | | |__   | |__) |  | |_) | |  | | /  \  | |__) | |  | | (___    ║")
        utils.print_centered(r"║  | |    |  __|   / /\ \ | |  | |  __|  |  _  /   |  _ <| |  | |/ /\ \ |  _  /| |  | |\___ \   ║")
        utils.print_centered(r"║  | |____| |____ / ____ \| |__| | |____ | | \ \   | |_) | |__| / ____ \| | \ \| |__| |____) |  ║")
        utils.print_centered(r"║  |______|______/_/    \_\_____/|______||_|  \_\  |____/ \____/_/    \_\_|  \_\_____/|_____/   ║")
        utils.print_centered(r"║                                                                                               ║")
        utils.print_centered(r"╚══════════════════════════════════════════════ ▲ ══════════════════════════════════════════════╝")
        if not self.leaderboard:
            utils.print_centered("No scores yet.")
            utils.print_centered("Press enter for new participant...")
            input()
            return
        sortedScores = sorted(self.leaderboard.items(), key=lambda x: x[1]["AverageScore"], reverse=True)
        self.showLeaderboardHeader()
        for i, (name, data) in enumerate(sortedScores, 1):
            scores = [data['Station1(R)'], data['Station2(F)'], data['Station3(D)'], data['Station4(A)'], data['Station5(T)']]
            widths = [12, 12, 12, 12, 12]
            coloredCols = []
            plainCols = []
            for j, (score, w) in enumerate(zip(scores, widths)):
                color = SCORE_COLORS[j](score)
                plain = f"{score:.2f}"
                padded = plain.rjust(w)
                plainCols.append(padded)
                coloredCols.append(f"{Style.BRIGHT}{color}{padded}{Style.RESET_ALL}")

            nameCol = f"{i}. {name.capitalize()}"
            avgCol  = f"{data['AverageScore']:>12.2f}"

            plainRow = (f"{nameCol:<20} | "
                    f"{plainCols[0]} | "
                    f"{plainCols[1]} | "
                    f"{plainCols[2]} | "
                    f"{plainCols[3]} | "
                    f"{plainCols[4]} | "
                    f"{avgCol}")

            coloredRow = (f"{nameCol:<20} | "
                      f"{coloredCols[0]} | "
                      f"{coloredCols[1]} | "
                      f"{coloredCols[2]} | "
                      f"{coloredCols[3]} | "
                      f"{coloredCols[4]} | "
                      f"{avgCol}")

            width = os.get_terminal_size().columns
            padding = (width - len(plainRow)) // 2
            print(" " * padding + coloredRow)

        utils.print_centered("Press enter for new participant...")
        input()

    def updateLeaderboard(self, name, scoresList, avgScore):
        name = name.lower()
        if name not in self.leaderboard or avgScore > self.leaderboard[name]["AverageScore"]:
            self.leaderboard[name] = {
                "Station1(R)": scoresList[0],
                "Station2(F)": scoresList[1],
                "Station3(D)": scoresList[2],
                "Station4(A)": scoresList[3],
                "Station5(T)": scoresList[4],
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
                else:
                    utils.print_centered("Invalid input, try again.")

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

            tests = [ReflexTest(arduino), ForceTest(arduino), DistanceTest(arduino), AnglePerceptionTest(arduino), TimePerceptionTest(arduino)]
            results = []
            for test in tests:
                utils.print_centered("Test beginning in 5 seconds, Get Ready.")
                time.sleep(5)
                test.beginTest()
                results.append(test.calculateScore())

            avg = (results[1] + results[2] + results[3] + results[4]) / 4
            newBest = ui.updateLeaderboard(name, results, avg)
            ui.showResults(name.capitalize(), results, avg, newBest)
            ui.displayLeaderboard()

    finally:
        utils.clear()
        utils.print_centered("Exiting the ENGINEER BENCHMARK. Goodbye.")
        ser.close()

if __name__ == "__main__":
    main()

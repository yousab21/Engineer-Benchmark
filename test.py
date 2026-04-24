import time
import json
import os
from colorama import Fore, Back, Style, init
init()

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

SCORE_COLORS = [reflexColor, percentColor, percentColor, percentColor, percentColor]

#===============================================
class UI:
    def __init__(self, leaderboard):
        self.leaderboard = leaderboard

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
            rank = sum(1 for person in self.leaderboard.values() if person["AverageScore"] > avg) + 1
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
        utils.print_centered(r"╚════════════════════════════════════════════ ▲ ════════════════════════════════════════════════╝")
        utils.print_centered("")
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
            return True
        return False

#===============================================
FAKE_LEADERBOARD = {
    "yousab": {"Station1(R)": 185.0, "Station2(F)": 95.0, "Station3(D)": 92.0, "Station4(A)": 88.0, "Station5(T)": 91.0, "AverageScore": 91.5},
    "ahmad":  {"Station1(R)": 310.0, "Station2(F)": 78.0, "Station3(D)": 65.0, "Station4(A)": 70.0, "Station5(T)": 60.0, "AverageScore": 68.25},
    "omar":   {"Station1(R)": 250.0, "Station2(F)": 85.0, "Station3(D)": 80.0, "Station4(A)": 76.0, "Station5(T)": 82.0, "AverageScore": 80.75},
    "yehia":  {"Station1(R)": 190.0, "Station2(F)": 60.0, "Station3(D)": 55.0, "Station4(A)": 50.0, "Station5(T)": 58.0, "AverageScore": 55.75},
}

FAKE_SESSION_SCORES = [210.0, 88.0, 92.0, 70.0, 95.0]
FAKE_SESSION_AVG    = (88.0 + 92.0 + 70.0 + 95.0) / 4

def main():
    ui = UI(FAKE_LEADERBOARD)

    while True:
        ans = ui.welcomeScreen()

        if ans == "1":
            # showWelcomeBack for a returning user
            ui.showWelcomeBack("Yousab", FAKE_LEADERBOARD["yousab"])
            # session results — new best
            ui.showResults("Yousab", FAKE_SESSION_SCORES, FAKE_SESSION_AVG, isNewBest=True)
            # session results — not a new best
            ui.showResults("Ahmad", FAKE_SESSION_SCORES, 55.0, isNewBest=False)

        elif ans == "2":
            ui.displayLeaderboard()

        elif ans == "3":
            # empty leaderboard screen
            ui_empty = UI({})
            ui_empty.displayLeaderboard()

        elif ans == "q":
            break
        else:
            utils.print_centered("Invalid input, try again.")

if __name__ == "__main__":
    main()

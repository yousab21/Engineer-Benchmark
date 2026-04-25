import serial
import serial.tools.list_ports
import time
import os
from colorama import Fore, Back, Style, init
init()

BAUD = 115200

#=======================================
class Utils:
    def clear(self):
        print("\033[H\033[J", end="")

    def print_centered(self, value, end="\n"):
        width = os.get_terminal_size().columns
        print(str(value).center(width), end=end)

utils = Utils()

#=======================================
def hrColor(pct):
    if pct < 10:   return Fore.GREEN
    elif pct < 25: return Fore.YELLOW
    else:          return Fore.RED

#=======================================
class ESP32_Handler:
    def __init__(self, bluetooth):
        self.bluetooth = bluetooth

    def readResponse(self):
        try:
            attempts = 0
            while attempts < 20:
                line = self.bluetooth.readline().decode('utf-8').strip()
                if line:
                    return line
                attempts += 1
            utils.print_centered("Timed out waiting for ESP32.")
            return None
        except serial.SerialException:
            utils.print_centered("ESP32 disconnected!")
            return None
        except UnicodeDecodeError:
            utils.print_centered("Received bad data, retrying...")
            return self.readResponse()

    def waitFor(self, expected):
        while True:
            line = self.readResponse()
            if line is None:
                continue
            if line == expected:
                return
            utils.print_centered(f"ESP32: {line}")

    def sendRequest(self, request):
        self.bluetooth.reset_input_buffer()
        self.bluetooth.write(f'{request}\n'.encode())

    def beginMonitoring(self):
        self.sendRequest("START")
        self.waitFor("BASELINE_COLLECTING")
        utils.print_centered(f"{Fore.YELLOW}Collecting baseline... keep still.{Style.RESET_ALL}")
        self.waitFor("READY")

    def endMonitoring(self):
        self.sendRequest("STOP")
        response = self.readResponse()
        if response is None or "ERR" in response:
            utils.print_centered(f"{Fore.RED}Sensor error: {response}{Style.RESET_ALL}")
            return None
        try:
            return float(response)
        except ValueError:
            utils.print_centered(f"{Fore.RED}Bad response: {response}{Style.RESET_ALL}")
            return None

#=======================================
def findPort():
    """Try to auto-detect the ESP32 COM port."""
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "CP210" in p.description or "CH34" in p.description or "USB" in p.description.upper():
            return p.device
    return None

def connectESP():
    utils.print_centered("Scanning for ESP32...")
    port = findPort()
    if port:
        utils.print_centered(f"Found device on {port}")
    else:
        utils.print_centered("Could not auto-detect port. Enter COM port manually (e.g. COM5): ", end="")
        port = input().strip()

    try:
        bluetooth = serial.Serial(port, BAUD, timeout=3)
        time.sleep(2)
        bluetooth.reset_input_buffer()
        utils.print_centered(f"{Fore.GREEN}Connected to {port}{Style.RESET_ALL}")
        return bluetooth
    except serial.SerialException as e:
        utils.print_centered(f"{Fore.RED}Failed to connect: {e}{Style.RESET_ALL}")
        raise

#=======================================
def printBanner():
    utils.clear()
    utils.print_centered(r"╔══════════════════════════════════════════════════════════════════════════════════════════════════╗")
    utils.print_centered(r"║    _____ _______ _____  ______  _____ _____     __  __  ____  _   _ _____ _______ ____  _____    ║")
    utils.print_centered(r"║   / ____|__   __|  __ \|  ____|/ ____/ ____|   |  \/  |/ __ \| \ | |_   _|__   __/ __ \|  __ \   ║")
    utils.print_centered(r"║  | (___    | |  | |__) | |__  | (___| (___     | \  / | |  | |  \| | | |    | | | |  | | |__) |  ║")
    utils.print_centered(r"║   \___ \   | |  |  _  /|  __|  \___ \\___ \    | |\/| | |  | | . ` | | |    | | | |  | |  _  /   ║")
    utils.print_centered(r"║   ____) |  | |  | | \ \| |____ ____) |___) |   | |  | | |__| | |\  |_| |_   | | | |__| | | \ \   ║")
    utils.print_centered(r"║  |_____/   |_|  |_|  \_\______|_____/_____/    |_|  |_|\____/|_| \_|_____|  |_|  \____/|_|  \_\  ║")
    utils.print_centered(r"║                                                                                                  ║")
    utils.print_centered(r"╚═══════════════════════════════════════════════ ▲ ════════════════════════════════════════════════╝")
    print()

def printResult(pct):
    utils.clear()
    print()
    print()
    color = hrColor(pct)
    utils.print_centered(f"{'=' * 45}")
    utils.print_centered("Heart Rate Trial Result")
    utils.print_centered(f"{'=' * 45}")
    print()

    plainText  = f"Heart Rate Increase:  {pct:.2f}%"
    width      = os.get_terminal_size().columns
    pctStr     = f"{pct:.2f}"
    colored    = plainText.replace(pctStr, f"{Style.BRIGHT}{color}{pctStr}{Style.RESET_ALL}")
    print(colored.center(width))
    print()

    if pct < 10:
        utils.print_centered(f"{Style.BRIGHT}{Fore.GREEN}Cool as a cucumber — barely broke a sweat !{Style.RESET_ALL}")
    elif pct < 25:
        utils.print_centered(f"{Style.BRIGHT}{Fore.YELLOW}Stress is showing — heart knows what's up.{Style.RESET_ALL}")
    else:
        utils.print_centered(f"{Style.BRIGHT}{Fore.RED}Heart's going full Egyptian WIFI mode !{Style.RESET_ALL}")

    print()
    utils.print_centered(f"{'=' * 45}")

#=======================================
def main():
    printBanner()
    utils.print_centered("Engineer Benchmark — Heart Rate Monitor")
    utils.print_centered("Standalone stress measurement tool")
    print()

    bluetooth = connectESP()
    esp = ESP32_Handler(bluetooth)

    utils.print_centered(f"Commands: {Style.BRIGHT}start{Style.RESET_ALL} — begin monitoring  |  {Style.BRIGHT}quit{Style.RESET_ALL} — exit")
    print()

    try:
        while True:
            utils.print_centered("> ", end="")
            cmd = input().strip().lower()

            if cmd == "quit":
                break

            elif cmd == "start":
                utils.clear()
                print()
                utils.print_centered(f"{Style.BRIGHT}Starting heart rate monitoring...{Style.RESET_ALL}")
                utils.print_centered("Place finger on sensor firmly.")
                print()

                esp.beginMonitoring()

                utils.clear()
                print()
                utils.print_centered(f"{Style.BRIGHT}{Fore.GREEN}Baseline locked — monitoring active !{Style.RESET_ALL}")
                print()
                utils.print_centered(f"Type {Style.BRIGHT}stop{Style.RESET_ALL} when the trial is over.")
                print()

                # wait for stop
                while True:
                    utils.print_centered("> ", end="")
                    inner = input().strip().lower()
                    if inner == "stop":
                        break
                    else:
                        utils.print_centered(f"Unknown command. Type {Style.BRIGHT}stop{Style.RESET_ALL} to end the trial.")

                utils.print_centered("Retrieving result...")
                pct = esp.endMonitoring()

                if pct is not None:
                    printResult(pct)
                else:
                    utils.print_centered(f"{Fore.RED}Could not retrieve a valid result.{Style.RESET_ALL}")

                print()
                utils.print_centered(f"Type {Style.BRIGHT}start{Style.RESET_ALL} for a new trial or {Style.BRIGHT}quit{Style.RESET_ALL} to exit.")
                print()

            else:
                utils.print_centered(f"Unknown command. Type {Style.BRIGHT}start{Style.RESET_ALL} or {Style.BRIGHT}quit{Style.RESET_ALL}.")

    finally:
        utils.clear()
        utils.print_centered("Closing connection. Goodbye.")
        bluetooth.close()

if __name__ == "__main__":
    main()

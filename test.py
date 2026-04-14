import serial
import time

PORT = '/dev/ttyUSB0'
BAUD = 9600

print("Opening port...")
ser = serial.Serial(PORT, BAUD, timeout=5)
print("Port opened, waiting 2s...")
time.sleep(2)
ser.reset_input_buffer()
print("Sending keyword...")
ser.write(b'FORCE_TEST\n')
print("Waiting for response...")
line = ser.readline()
print(f"Got: {line}")
ser.close()

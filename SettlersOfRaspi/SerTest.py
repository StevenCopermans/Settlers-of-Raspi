import serial
import time
import json


class SerialRaspberry:
    def __init__(self):
        self.port = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

    def send_message(self, message):
        msg = message + "\n"
        self.port.write(msg.encode('utf-8'))

    def read_message(self):
        return self.port.readline().decode('utf-8', errors='ignore').split('\n')[0]

    def available(self):
        return self.port.inWaiting()


class Serial:
    def __init__(self):
        self.ser = SerialRaspberry()

    def run(self):
        print("HAH")
        while True:
            self.ser.send_message("hi")
            if self.ser.available():
                print("WTF")
                print(self.ser.read_message())

ser = Serial()
ser.run()

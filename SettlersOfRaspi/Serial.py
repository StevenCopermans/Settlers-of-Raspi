import serial
import time
from threading import Thread
import json


class SerialRaspberry:
    def __init__(self):
        self.port = serial.Serial('/dev/serial0', baudrate=115200, timeout=0)

    def send_message(self, message):
        msg = message + "\n"
        self.port.write(msg.encode('utf-8'))

    def read_message(self):
        return self.port.readline().decode('utf-8', errors='ignore').split('\n')[0]

    def available(self):
        return self.port.inWaiting()


class Serial(Thread):
    def __init__(self):

        self.ser = SerialRaspberry()

        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            time.sleep(0.3)
            while self.ser.available():
                print(self.ser.read_message())

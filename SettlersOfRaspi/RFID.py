from threading import Thread
import time

from mfrc522 import SimpleMFRC522


class RFID(Thread):
    def __init__(self):
        self.reader = SimpleMFRC522()

        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            print("I RUN")
            id, text = self.reader.read()
            print(id)
            print(text)

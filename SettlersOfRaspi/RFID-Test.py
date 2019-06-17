from mfrc522 import SimpleMFRC522


class RFID:
    def __init__(self):
        self.reader = SimpleMFRC522()
    def run(self):
        while True:
            print("I RUN")
            id, text = self.reader.read()
            print(id)
            print(text)

test = RFID()
test.run()
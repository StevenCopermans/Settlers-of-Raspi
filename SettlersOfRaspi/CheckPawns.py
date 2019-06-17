from threading import Thread
from MCP23017 import MCP23017
import smbus
import time


class CheckPawns(Thread):
    def __init__(self, socket, conn):
        self.conn = conn
        self.buttons = []
        for i in range(126):
            self.buttons.append(0)

        self.buttonIndexes = [10, 9, 8, 15, 5, 6, 7, 35, 36, -1, -1, -1, -1, 11, 4, 37, -1, 14, 13, 12, 0, 1, 2, 3, 50, 48, 39, 38, -1, -1, -1, -1, -1, -1, 23, 55, 49, -1, -1, -1, -1, 22, 21, 20, 19, 54, 53, 63, 52, 51]

        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.socket = socket
        self.bus = smbus.SMBus(1)

        for i in range(8):
            for j in range(2):
                try:
                    self.bus.write_byte_data(MCP23017.ADDRESS.value + i, MCP23017.IODIRA.value + j, 0xFF)
                    self.bus.write_byte_data(MCP23017.ADDRESS.value + i, MCP23017.GPPUA.value + j, 0xFF)
                    self.bus.write_byte_data(MCP23017.ADDRESS.value + i, MCP23017.IPOLA.value + j, 0xFF)
                except:
                    pass

    def run(self):
        while True:
            time.sleep(5)
            for i in range(8):
                for j in range(2):
                    try:
                        buttons = self.bus.read_byte_data(MCP23017.ADDRESS.value + i, MCP23017.GPIOA.value + j)
                        for x in range(8):
                            try:
                                if (buttons >> x & 1) != self.buttons[self.buttonIndexes.index(i*16 + j*8 + x)]:
                                    self.buttons[self.buttonIndexes.index(i*16 + j*8 + x)] = buttons >> x & 1
                                    self.socket.emit("GO", [self.buttonIndexes.index(i*16 + j*8 + x), buttons >> x & 1])
                                    self.conn.set_data(
                                        'INSERT INTO mydb.Historiek (SensorID, Value) VALUES(%s, %s);',
                                        [self.buttonIndexes.index(i*16 + j*8 + x), "Pressed" if buttons >> x & 1 else "Released"]
                                    )
                            except:
                                pass
                    except:
                        pass

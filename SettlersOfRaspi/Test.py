from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from RPi import GPIO
from CheckPawns import CheckPawns
from Serial import Serial
from Database import Database
import json
import pigpio

GPIO.setmode(GPIO.BCM)

# INIT THE APP
app = Flask(__name__)

# SETTINGS
CORS(app)
app.config['SECRET_KEY'] = 'Secret!'
socket = SocketIO(app)
conn = Database(app=app, user='steven', password='lolol', db='mydb')

Serial()
CheckPawns(socket, conn)

ledColor = '00FFFF'
ledMode = 'auto'
ledPins = [5, 17, 27]

piGPIO = pigpio.pi()

for i in range(3):
    piGPIO.set_PWM_frequency(ledPins[i], 500)
    piGPIO.set_PWM_dutycycle(ledPins[i], 0)


@socket.on('connect')
def connect():
    print("connected")
    socket.emit('ledColor', ledColor)


@socket.on('sensors')
def getSensors():
    print("I wanna get sensors")
    sensors = conn.get_data('SELECT EntryID, mydb.Historiek.SensorID, Time, Value, Name FROM mydb.Historiek INNER JOIN mydb.Sensor ON mydb.Historiek.SensorID = mydb.Sensor.SensorID INNER JOIN mydb.SensorType ON mydb.Sensor.TypeID = mydb.SensorType.TypeID ORDER BY EntryID DESC LIMIT 100;')
    print(sensors)
    socket.emit("SensorData", json.dumps(sensors, default=str))


@socket.on('changeColor')
def changeColor(value):
    global socket
    global ledColor
    print("I was called?")
    ledColor = value.lstrip('#')

    for i in (0, 2, 4):
        temp = int(value[i:i + 2], 16)
        piGPIO.set_PWM_dutycycle(ledPins[int(i/2)], temp)

    socket.emit('ledColor', ledColor)

# START THE APP
if __name__ == '__main__':
    changeColor(ledColor)
    socket.run(app, debug=False, host="0.0.0.0", port=5000)

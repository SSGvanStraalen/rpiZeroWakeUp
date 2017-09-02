import unicornhat as uh
import time
import datetime
import threading

from flask import Flask, request, send_from_directory
from persistor import DataPersistor
from theWeather import TheWeatherMan
app = Flask(__name__)

uh.set_layout(uh.PHAT)
uh.brightness(0.5)

config = DataPersistor.loadData('data.json')

def setColor (r, g, b):
    "this sets the color on the unicorn"
    for x in range(8):
        for y in range(4):
            uh.set_pixel(x, y, r, g, b)
    uh.show()
    return

def clearLights ():
    uh.clear()
    return

def getWeatherAndSetColor ():
    code = TheWeatherMan.getTodaysWeather()['code']
    r = config['weather'][code]['color']['r']
    g = config['weather'][code]['color']['g']
    b = config['weather'][code]['color']['b']
    setColor(r, g, b)
    return code

@app.route('/<path:path>')
def index(path):
    return send_from_directory('public', path)

@app.route('/testGetWeather')
def testGetWeather():
    return getWeatherAndSetColor()

@app.route('/getConfig')
def getConfig():
    return config;

@app.route('/getWeather')
def getWeather():
    return TheWeatherMan.getTodaysWeather()['code'];

@app.route('/setConfig', methods=['POST'])
def setConfig():
    DataPersistor.saveData('data.json', request.get_json())
    config = request.get_json()
    return 'done'

@app.route('/setColortje', methods=['POST'])
def setColortje():
    if request.method == 'POST':
        rgb =  request.get_json();
        r = int(request.get_json()['r'])
        g = int(request.get_json()['g'])
        b = int(request.get_json()['b'])
        setColor(r, g, b)
    return 'done'

@app.route('/setAlarm')
def setAlarm():
    now = datetime.datetime.now()
    alarm_time = datetime.datetime.combine(now.date(), datetime.time(6, 45, 0))
    timeCountdown = (alarm_time - now).total_seconds()

    if timeCountdown <= 0:
        timeCountdown = (alarm_time + datetime.timedelta(days=1) - now).total_seconds()

    t = threading.Timer(timeCountdown ,getWeatherAndSetColor)
    t.start()
    return 'timeSet now and alarm_time'


@app.route('/stopAlarm')
def stopAlarm():
    setColor(0, 0, 0)
    return 'cleared the pi'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

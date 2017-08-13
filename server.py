import unicornhat as uh
import time
import datetime
import threading

from flask import Flask, request, send_from_directory
from flask import request
app = Flask(__name__)

uh.set_layout(uh.PHAT)
uh.brightness(0.5)

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

@app.route('/<path:path>')
def index(path):
    setColor(0, 255, 255)
    return send_from_directory('public', path)


@app.route('/setColortje', methods=['POST'])
def setColortje():
    if request.method == 'POST':
        rgb =  request.get_json();
        setColor(rgb[r], rgb[g], rgb[b])
        print ('test')
        print (request.data)
        print (request.get_json())
    else:
        print ('geen ideee')

    return 'hi'


@app.route('/setAlarm')
def setAlarm():
    now = datetime.datetime.now()
    alarm_time = datetime.datetime.combine(now.date(), datetime.time(6, 45, 0))
    timeCountdown = (alarm_time - now).total_seconds()

    if timeCountdown <= 0:
        timeCountdown = (alarm_time + datetime.timedelta(days=1) - now).total_seconds()

    t = threading.Timer(timeCountdown ,setColor, [0, 255, 255])
    t.start()
    return 'timeSet now and alarm_time'


@app.route('/stopAlarm')
def stopAlarm():
    setColor(0, 0, 0)
    return 'cleared the pi'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# Simple utility which connects to udacity self driving car simulator and determines if the car is on the road

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask
import time

sio = socketio.Server()
app = Flask(__name__)

@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        print(data['is_on_road'])
    send_control(0, 1)
	
def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)
		
@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    #while True:
    send_control(0, 0)
    #time.sleep(2)


if __name__ == "__main__":
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
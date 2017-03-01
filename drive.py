# Simple utility which connects to udacity self driving car simulator and determines if the car is on the road
import base64
from datetime import datetime
import os
import time
import shutil

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO


sio = socketio.Server()
app = Flask(__name__)
counter = 0

@sio.on('telemetry')
def telemetry(sid, data):
    global counter
    if data:
        print(data['is_on_road'])
        counter += 1
        if counter > 50:
            '''
            image = Image.open(BytesIO(base64.b64decode(data['C:/Users/Itai Caspi/Documents/udacity_sdc/images'])))
            image_array = np.asarray(image)
            timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            image_filename = os.path.join('C:/Temp/', timestamp)
            print('saving to ' + image_filename)
            image.save('{}.jpg'.format(image_filename))
            '''
            reset()
            counter = 0
    send_control(0, 1)
	

def reset():
    print("reseting environment")
    sio.emit("reset", data={}, skip_sid=True)

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
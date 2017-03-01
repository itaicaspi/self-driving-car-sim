# Simple utility which connects to udacity self driving car simulator and determines if the car is on the road
import base64
from datetime import datetime
import os
import time
import shutil
import sys

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
import threading

#eventlet.monkey_patch(thread=True)
sio = socketio.Server()
app = Flask(__name__)
_env = []

class Environment:
	def __init__(self, action_type="continuous"):
		global _env
		_env = self

		# initialize car parameters
		self.steering_angle = 0
		self.throttle = 0
		self.speed = 0
		self.is_on_road = True
		self.observation = []
		self.action = "None"
		self.waiting_for_action_execution = False

		# action space
		self.steering_delta = 0.01
		self.throttle_delta = 0.1
		self.action_type = action_type
		if self.action_type == "continuous":
			self.action_space = []
		elif self.action_type == "discrete":
			self.action_space = {
				"None": [0, 0],
				"Left": [-self.steering_delta, 0],
				"Right": [self.steering_delta, 0],
				"Up": [0, self.throttle_delta], 
				"Down": [0, -self.throttle_delta]
			}
			
		# server communication
		self.is_connected = False
		self.connect()


	def step(self, action):
		self.action = action
		print(_env.steering_angle, _env.throttle, _env.speed, _env.is_on_road)
		self.waiting_for_action_execution = True
		while self.waiting_for_action_execution:
			pass
		return self.steering_angle, self.throttle, self.speed, self.is_on_road

	def _step(self, action):
		if action == None:
			return

		self.action = action
		# update control values
		if self.action_type == "discrete":
			action = self.action_space[action]

		steering_angle = self.steering_angle + action[0]
		throttle = self.throttle + action[1]

		# send to game server
		sio.emit("steer", data={'steering_angle': steering_angle.__str__(), 'throttle': throttle.__str__()})

	def reset(self):
		# reset environment
		sio.emit("reset", data={}, skip_sid=True)

	def serve_app(self, sio, app):
		app = socketio.Middleware(sio, app)
		eventlet.wsgi.server(eventlet.listen(('', 4567)), app)

	def connect(self):
		print("Connecting to game server")
		wst = threading.Thread(target=self.serve_app, args=(sio, app))
		wst.daemon = True
		wst.start()
		while not self.is_connected:
			pass

@sio.on('telemetry')
def telemetry(sid, data):
	global _env
	_env.steering_angle = float(data["steering_angle"])
	_env.throttle = float(data["throttle"])
	_env.speed = float(data["speed"])
	_env.is_on_road = data["is_on_road"]
	_env.observation = data["image"]
	_env._step(_env.action)
	_env.waiting_for_action_execution = False
	#_env.action = None

@sio.on('connect')
def connect(sid, environ):
	global _env
	print("Connect to ", sid)
	_env.is_connected = True
	_env._step("None")

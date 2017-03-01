from environment import *
import time
import random
env = Environment("discrete")
if __name__ == "__main__":
	env = Environment("discrete")
	while True:
		#env.action = random.choice(list(env.action_space.keys()))
		env.step("Up")
		time.sleep(0.3)
		pass
		#env.step("Left")


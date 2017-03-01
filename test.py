from environment import Environment
import time

if __name__ == "__main__":
	env = Environment("discrete")
	while True:
		env.step("Up")
		time.sleep(1)
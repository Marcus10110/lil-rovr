from adafruit_servokit import ServoKit
from time import sleep
kit = ServoKit(channels=16)

servos = range(4)
for angle in range(0, 180, 1):
    for servo in servos:
        kit.servo[servo].angle = angle
        sleep(1.0/180)

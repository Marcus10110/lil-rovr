from typing import TypedDict
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit
from time import sleep
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import the RFM69 radio module.
import adafruit_rfm69


class MotionData(TypedDict):
    servo_front_left: float
    servo_front_right: float
    servo_back_left: float
    servo_back_right: float

    motor_front_left: float
    motor_front_right: float
    motor_center_left: float
    motor_center_right: float
    motor_back_left: float
    motor_back_right: float


servo_kit = ServoKit(channels=16)
motor_kits = [MotorKit(0x60), MotorKit(0x61)]

servo_front_left = servo_kit.servo[0]
servo_front_right = servo_kit.servo[1]
servo_back_left = servo_kit.servo[2]
servo_back_right = servo_kit.servo[3]

all_steering_servos = [servo_front_left,
                       servo_front_right, servo_back_left, servo_back_right]

pan_servo = servo_kit.servo[4]
tilt_servo = servo_kit.servo[5]

all_pan_tilt_servos = [pan_servo, tilt_servo]

motor_front_left = motor_kits[0].motor1
motor_front_right = motor_kits[0].motor2
motor_center_left = motor_kits[0].motor3
motor_center_right = motor_kits[0].motor4
motor_back_left = motor_kits[1].motor1
motor_back_right = motor_kits[1].motor2

all_motors = [motor_front_left, motor_front_right, motor_center_left,
              motor_center_right, motor_back_left, motor_back_right]


# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height


# RFM69 Configuration
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)


def set_motion_data(data: MotionData):
    servo_front_left.angle = data['servo_front_left']
    servo_front_right.angle = data['servo_front_right']
    servo_back_left.angle = data['servo_back_left']
    servo_back_right.angle = data['servo_back_right']

    motor_front_left.throttle = data['motor_front_left']
    motor_front_right.throttle = data['motor_front_right']
    motor_center_left.throttle = data['motor_center_left']
    motor_center_right.throttle = data['motor_center_right']
    motor_back_left.throttle = data['motor_back_left']
    motor_back_right.throttle = data['motor_back_right']


def reset():
    data = MotionData()
    data['servo_front_left'] = 90
    data['servo_front_right'] = 90
    data['servo_back_left'] = 90
    data['servo_back_right'] = 90
    data['motor_front_left'] = 0
    data['motor_front_right'] = 0
    data['motor_center_left'] = 0
    data['motor_center_right'] = 0
    data['motor_back_left'] = 0
    data['motor_back_right'] = 0
    set_motion_data(data)
    # reset the pan tilt servos too
    for servo in all_pan_tilt_servos:
        servo.angle = 90


reset()
print('Hardware initialized')

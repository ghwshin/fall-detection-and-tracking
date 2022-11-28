import Jetson.GPIO as GPIO
import time


class MotorControler:
    SERVO_PIN = 33
    STOP = 7.5
    LEFT = 7.0
    RIGHT = 8.0
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)

        # 50Hz
        self.pwm = GPIO.PWM(self.SERVO_PIN, 50)
        print('PWM initialized')

    # 360 degrees
    # 1.4 ~ 7.2 : clockwise
    # 7.3 ~ 7.6 : stop
    # 7.7 ~ 13.4 : counterclockwise
    def start_motor(self):
        self.pwm.start(7.5)
        print('Servo Motor Started')

    def stop_motor(self):
        self.pwm.ChangeDutyCycle(7.5)

    # direction True : 정방향(LEFT)
    # direction False : 역방향(RIGHT)
    def moving_motor(self, direction, inverse=False):
        if direction:
            if inverse:
                self.pwm.ChangeDutyCycle(self.RIGHT)
            else:
                self.pwm.ChangeDutyCycle(self.LEFT)
        else:
            if inverse:
                self.pwm.ChangeDutyCycle(self.LEFT)
            else:
                self.pwm.ChangeDutyCycle(self.RIGHT)
        time.sleep(0.1)
        self.stop_motor()

    def end_motor(self):
        print('Ending Servo Motor...')
        self.pwm.stop()
        GPIO.cleanup()

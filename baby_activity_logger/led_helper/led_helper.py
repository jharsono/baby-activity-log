import RPi.GPIO as GPIO

class LEDHelper:
    def __init__(self, red_pin, green_pin, blue_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)

        self.red = GPIO.PWM(red_pin, 1000)
        self.green = GPIO.PWM(green_pin, 1000)
        self.blue = GPIO.PWM(blue_pin, 1000)

        self.red.start(0)
        self.green.start(0)
        self.blue.start(0)

    def set_color(self, rgb=[]):
        self.red.start(0)
        self.green.start(0)
        self.blue.start(0)

        # The line below should allow you to use web-like RGB values from 0-255,
        # but currently causes flickering with 470ohm resistors

        # rgb = [(x / 255.0) * 100 for x in rgb]

        self.red.ChangeDutyCycle(rgb[0])
        self.green.ChangeDutyCycle(rgb[1])
        self.blue.ChangeDutyCycle(rgb[2])

    def off(self):
        self.red.stop()
        self.green.stop()
        self.blue.stop()

    def set_fetch_status(self):
        self.set_color([1, 0, 1])

    def set_success_status(self):
        self.set_color([0, 1, 0])

    def set_fail_status(self):
        self.set_color([1, 0, 0])
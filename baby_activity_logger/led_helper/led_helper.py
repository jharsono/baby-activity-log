import RPi.GPIO as GPIO

class LEDHelper:
    def __init__(self, red_pin, green_pin, blue_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)

        self.red = GPIO.PWM(red_pin, 100)
        self.green = GPIO.PWM(green_pin, 100)
        self.blue = GPIO.PWM(blue_pin, 100)

        self.red.start(100)
        self.green.start(100)
        self.blue.start(100)

    def set_color(self, rgb=[]):
        rgb = [(x / 255.0) * 100 for x in rgb]
        self.red.ChangeDutyCycle(rgb[0])
        self.green.ChangeDutyCycle(rgb[1])
        self.blue.ChangeDutyCycle(rgb[2])

    def light_off(self):
        self.red.stop()
        self.green.stop()
        self.blue.stop()
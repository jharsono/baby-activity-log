from time import sleep
import schedule
import RPi.GPIO as GPIO
from gcal_api_client.gcal_api_client import GcalApiClient
# from alert_button.alert_button import AlertButton

colors = {
    'purple': [1, 0, 1],
    'red': [1, 0, 0],
    'green': [0, 1, 0],
}

gpio_button_pins = {
    'sleep': 16,
    'eat': 20,
    'wake': 21,
    'call': 19,
}

gpio_pin_actions = {
    16: 'Sleep',
    20: 'Eat',
    21: 'Wake',
}

gpio_led_pins = {
    'red': 4,
    'green': 5,
    'blue': 6,
}

sleep_button = Button(gpio_button_pins['sleep'])
eat_button = Button(gpio_button_pins['eat'])
wake_button = Button(gpio_button_pins['wake'])
test_button = Button(19)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(gpio_led_pins['red'], GPIO.OUT)
GPIO.setup(gpio_led_pins['green'], GPIO.OUT)
GPIO.setup(gpio_led_pins['blue'], GPIO.OUT)

# set up colors with pwm
RED = GPIO.PWM(gpio_led_pins['red'], 100)
GREEN = GPIO.PWM(gpio_led_pins['green'], 100)
BLUE = GPIO.PWM(gpio_led_pins['blue'], 100)
RED.start(0)
GREEN.start(0)
BLUE.start(0)

LIGHTS = [RED, GREEN, BLUE]

# Set up the call button
# call_button = AlertButton(gpio_button_pins['call'])


# Set up the calendar API
# try:
#     cal = GcalApiClient('../settings/client_secret.json',
#                         '../settings/token.pkl')
#     print('Ready')
#     green.value = led_value
#     sleep(5)
#     green.off()
#     schedule.every(15).minutes.do(cal.set_last_sleep)
# except:
#     print('Error with gcal client, check settings files.')
#     red.on()

# Set color by giving RGB values in a list
def set_color(rgb=[]):
    # convert 0-255 range to 0-100
    rgb = [(x / 255.0) * 100 for x in rgb]
    RED.ChangeDutyCycle(rgb[0])
    GREEN.ChangeDutyCycle(rgb[1])
    BLUE.ChangeDutyCycle(rgb[2])

def light_off():
    print('light off')
    for light in LIGHTS:
        light.stop()

def pause():
    sleep(2)

# def dispatch_event(button):
#     pin_number = button.pin.number
#     event_name = gpio_pin_actions[pin_number]

#     blue.value = led_value

#     if event_name == 'Wake':
#         event = cal.end_sleep()
#         pause()
#     else:
#         event = cal.create_event(event_name)
#         pause()

#     print(event)

#     if not event:
#         blue.off()
#         red.value = led_value
#     else:
#         print('success')
#         blue.off()
#         green.value = led_value
#         pause()

#     light_off()

while True:
    sleep_button.when_pressed = \
        eat_button.when_pressed = \
        wake_button.when_pressed \
        = light_off

#     test_button.when_pressed = light_off
#     #  call_button.run()
#     # Checks whether a scheduled task
#     # is pending to run or not
#     schedule.run_pending()
#     sleep(5)

GPIO.cleanup()
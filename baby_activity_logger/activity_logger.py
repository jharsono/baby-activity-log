from time import sleep
import schedule
import RPi.GPIO as GPIO
from gpiozero import Button
from led_helper.led_helper import LEDHelper
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

# GPIO PINS
RED = 4
GREEN = 5
BLUE = 6

sleep_button = Button(gpio_button_pins['sleep'])
eat_button = Button(gpio_button_pins['eat'])
wake_button = Button(gpio_button_pins['wake'])
test_button = Button(19)

led = LEDHelper(RED, GREEN, BLUE)

# Set up the call button
# call_button = AlertButton(gpio_button_pins['call'])

# Set up the calendar API
try:
    cal = GcalApiClient('../settings/client_secret.json',
                        '../settings/token.pkl')
    print('Ready')
    led.set_success_status()
    sleep(5)
    led.off()
    schedule.every(15).minutes.do(cal.set_last_sleep)
except:
    print('Error with gcal client, check settings files.')
    led.set_fail_status()


def pause():
    sleep(2)

def dispatch_event(button):
    pin_number = button.pin.number
    event_name = gpio_pin_actions[pin_number]
    led.set_fetch_status()

    if event_name == 'Wake':
        event = cal.end_sleep()
        pause()
    else:
        event = cal.create_event(event_name)
        pause()

    print(event)

    if not event:
        led.set_fail_status()
    else:
        print('success')
        led.set_success_status()
        pause()
        led.off()

while True:
    sleep_button.when_pressed = \
        eat_button.when_pressed = \
        wake_button.when_pressed \
        = dispatch_event

#     test_button.when_pressed = light_off
#     #  call_button.run()
#     # Checks whether a scheduled task
#     # is pending to run or not
    schedule.run_pending()
    sleep(5)

GPIO.cleanup()
from time import sleep
import schedule
from gpiozero import RGBLED, PWMLED, Button
from gcal_api_client.gcal_api_client import GcalApiClient
from alert_button.alert_button import AlertButton

colors = {
    'purple': (1, 0, 1),
    'red': (1, 0, 0),
    'green': (0, 1, 0),
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
test_button = Button(26)
red = PWMLED(4)
green = PWMLED(5)
blue = PWMLED(6)

# make the LED dimmer
led_value = 0.1

# Set up the call button
call_button = AlertButton(gpio_button_pins['call'])
call_button.run()

# Set up the calendar API
try:
    cal = GcalApiClient('../settings/client_secret.json',
                        '../settings/token.pkl')
    print('Ready')
    green.value = led_value
    sleep(5)
    green.off()
except:
    print('Error with gcal client, check settings files.')
    red.on()

def light_off():
    green.off()
    red.off()
    blue.off()

def pause():
    sleep(2)

def dispatch_event(button):
    pin_number = button.pin.number
    event_name = gpio_pin_actions[pin_number]

    blue.value = led_value

    if event_name == 'Wake':
        event = cal.end_sleep()
        pause()
    else:
        event = cal.create_event(event_name)
        pause()

    print(event)

    if not event:
        blue.off()
        red.value = led_value
    else:
        print('success')
        blue.off()
        green.value = led_value
        pause()

    light_off()

# Scheduling the task
schedule.every(15).minutes.do(cal.set_last_sleep)

while True:
    sleep_button.when_pressed = \
        eat_button.when_pressed = \
        wake_button.when_pressed \
        = dispatch_event



    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    sleep(5)

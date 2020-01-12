from gpiozero import RGBLED, Button
from time import sleep
from gcal_api_client.gcal_api_client import GcalApiClient

colors = {
    'purple': (1, 0, 1),
    'red': (1, 0, 0),
    'green': (0, 1, 0),
}

gpio_button_pins = {
    'sleep': 16,
    'eat': 20,
    'wake': 21,
}

gpio_pin_actions = {
    16: 'sleep',
    20: 'eat',
    21: 'wake',
}

gpio_led_pins = {
    'red': 4,
    'green': 5,
    'blue': 6,
}

try:
    cal = GcalApiClient('../settings/client_secret.json', '../settings/token.pkl', '../settings/last_sleep.pkl')
    print('Ready')
except:
    print('Error with gcal client, check settings files.')

sleep_button = Button(gpio_button_pins['sleep'])
eat_button = Button(gpio_button_pins['eat'])
wake_button = Button(gpio_button_pins['wake'])
led = RGBLED(**gpio_led_pins)

def dispatch_event(button):
    pin_number = button.pin.number
    event_name = gpio_pin_actions[pin_number]

    led.blink(
        on_time=0.5, off_time=0.5, n=5, on_color=colors['purple']
    )
    if event_name == 'wake':
        event = cal.end_sleep()
        sleep(2)
    else:
        event = cal.create_event(event_name)
        sleep(2)

    print(event)

    if not event:
        led.color = colors['red']
    else:
        print('success')
        led.color = colors['green']
        sleep(2)
        led.off()

while True:
    sleep_button.when_pressed = dispatch_event
    eat_button.when_pressed = dispatch_event
    wake_button.when_pressed = dispatch_event
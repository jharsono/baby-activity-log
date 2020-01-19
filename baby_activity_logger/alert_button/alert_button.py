WAVFILE = '/home/pi/projects/baby-activity-logger/baby_activity_logger/alert_button/alert.wav'
import pygame
from pygame import *
import sys
from gpiozero import Button
from time import sleep
import os


class AlertButton:
    def __init__(self, gpio_pin):
        self.alert_on = False
        self.play_button = Button(gpio_pin)

        pygame.display.init()
        screen = pygame.display.set_mode((1,1))
        mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
        pygame.init()
        # screen=pygame.display.set_mode((400,400),0,32)


    def toggle_alert(self):
        self.alert_on = not self.alert_on

    def play_alert(self):
        s = pygame.mixer.Sound(WAVFILE)
        ch = s.play()
        while ch.get_busy():
            pygame.time.delay(100)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
           # pygame.display.update()

            self.play_button.when_pressed = self.toggle_alert

            while self.alert_on:
                self.play_alert()
                sleep(1)






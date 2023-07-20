import sys
import gpiozero
import logging
import time
from rpi_hardware_pwm import HardwarePWM
from pump import Pump

class Choice:
    def __init__(self, start_pin = 10, right_pin = 9, left_pin = 11):
        self.start_button = gpiozero.Button(start_pin)
        self.right_button = gpiozero.Button(right_pin)
        self.left_button = gpiozero.Button(left_pin)
        self.pump = Pump


    def startGame(self):
        print("Press the Start Button")
        self.start_button.wait_for_press()
        print("Starting!")
    

    def choice(self, option):
        while True:
            if ((self.right_button.is_pressed() and option=='Right') or (self.left_button.is_pressed() and option=='Left')):
                print("Reward Given!")
                pump.run_forward(50,5)
                break
            elif ((self.right_button.is_pressed() and option=='Right') or (self.left_button.is_pressed() and option=='Left')):
                print("Wrong Choice")
                break

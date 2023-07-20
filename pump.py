import sys
import gpiozero
import logging
import time
from rpi_hardware_pwm import HardwarePWM


class Pump:
    CW = 1
    CCW = -1
    def __init__(self, in1=17, in2=27, ena=0):
        """
        in1, in2 are the GPIO pins that connect to the in1 and in2 pins of the H-Bridge
        ena is the H/W PWM channel (0 or 1) that connects to the ena  pin of the H-Bridge
        PWM channel 0 is mapped to GPIO pin 18 and channel 1 is mapped to GPIO pin 19.
        """
        self.in1 = gpiozero.DigitalOutputDevice(in1)
        self.in2 = gpiozero.DigitalOutputDevice(in2)
        self.pwm = HardwarePWM(pwm_channel=ena, hz=60)
        self.speed = 0.0
        self.direction = Pump.CW
        self.pwm.stop()

    def set_speed(self,speed):
        if speed < 0.0 or speed > 100.0:
            raise Exception(f"Unsupported speed {speed}. Value should be >=0 and <= 100")
        self.speed = speed
        if speed == 0.0:
            self.pwm.stop()
        else:
            self.pwm.start(speed)

    def set_direction(self, direction):
        if direction == Pump.CW:
            self.direction = direction
            self.in1.on()
            self.in2.off()
        elif direction == Pump.CCW:
            self.direction = direction
            self.in1.off()
            self.in2.on()
        else:
            raise Exception(f"Unsupported direction {direction}")

    def stop(self):
        self.pwm.stop()
        self.in1.off()
        self.in2.off()


    def start(self, speed = None, direction=None):
        if speed is not None:
            self.set_speed(speed)
        if direction is not None:
            self.set_direction(direction)
        self.pwm.start(self.speed)


    def run_forward(self,speed, duration):
        if duration <= 0:
            raise Exception("duration must be a +ve value in seconds")
        self.start(speed=speed, direction=Pump.CW)
        time.sleep(duration)
        self.stop()


    def run_backward(self, speed, duration):
        if duration <= 0:
            raise Exception("duration must be a +ve value in seconds")
        self.start(speed=speed, direction=Pump.CCW)
        time.sleep(duration)
        self.stop()

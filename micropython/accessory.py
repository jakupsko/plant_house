""" controlls accessories, either motor or light control """

from machine import Pin
import utime

class Accessory:
    def __init__(self, accessory_pin:int):
        self.pin = Pin(accessory_pin, Pin.OUT)
        
    def turn_on(self, duration:int = 0):
        """ turns on motor for "duration" number of seconds. if unspecified then leaves it on """
        self.pin.value(1)
        
        if duration: # if duration is left blank, this part will not execute and accessory will stay on
            utime.sleep_ms(duration * 1000)
            self.turn_off()
        
    def turn_off(self):
        """ turns off motor """
        self.pin.value(0)
        

if __name__ == '__main__':
    motor = Accessory(3)
    
    motor.turn_on(1)
    

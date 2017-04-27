
#import copy
import math
#import sys
#import os 
from sense_hat import SenseHat 
import time

# the next elements instantiate a sensehat object, 
sense = SenseHat()
sense.clear()
sense.set_imu_config(True,False,False)
sense.low_light = True



def sensorget():
    sensordict = {'humidity': 0, 'temp':0, 'humidtemp':0, 'pressuretemp':0,'pressure':0,'compass':0} 
    sensordict['humidity'] = sense.get_humidity()
    sensordict['temp'] = sense.get_temperature()
    sensordict['humidtemp'] = sense.get_temperature_from_humidity()
    sensordict['pressuretemp'] = sense.get_temperature_from_pressure()
    sensordict['pressure'] = sense.get_pressure()
    sensordict['compass'] = sense.get_compass()
    return sensordict

def printscreen(sensordict):
    print("Temperature: %s C" % sensordict['temp'])
    print("Temperature from humidity: %s C" % sensordict['humidtemp'])
    print("Temperature from pressure: %s C" % sensordict['pressuretemp'])
    print("Pressure: %s Millibars" % sensordict['pressure'])
    print("Humidity: %s %%rH" % sensordict['humidity'])
    print("North: %s" % sensordict['compass'])

class led_display(object):
    def __init__(self):
        sense.clear()  # no arguments defaults to off 
        self.ticks = 0
        
    def animate(self):
        for x in range(8):
            for y in range(8):
                cx = x + 0.5*math.sin(self.ticks/5.0)
                cy = y + 0.5*math.cos(self.ticks/3.0)
                v = math.sin(math.sqrt(100*(math.pow(cx, 2.0)+math.pow(cy, 2.0))+1.0+self.ticks))
                #v = math.sin(x*10.0+self.ticks)
                v = (v + 1.0)/2.0
                v = int(v*255.0)
                sense.set_pixel(x,y,v,0,0)
        self.ticks = self.ticks+1
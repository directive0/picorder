from __future__ import division
import copy
import math
import sys
import os 
import psutil
import time




def sensorget():
    
   statusram = psutil.virtual_memory()
   
   sensordict = {'humidity': 0, 'temp':0, 'humidtemp':0, 'pressuretemp':0,'pressure':0,'compass':0} 
   sensordict['humidity'] = psutil.cpu_percent()
   sensordict['temp'] = statusram[2]
   sensordict['humidtemp'] = psutil.cpu_percent()
   sensordict['pressuretemp'] = psutil.cpu_percent()
   sensordict['pressure'] = psutil.cpu_percent()
   sensordict['compass'] = psutil.cpu_percent()
   return sensordict

def printscreen(sensordict):
   print("Temperature: %s C" % sensordict['temp'])
   print("Temperature from humidity: %s C" % sensordict['humidtemp'])
   print("Temperature from pressure: %s C" % sensordict['pressuretemp'])
   print("Pressure: %s Millibars" % sensordict['pressure'])
   print("Humidity: %s %%rH" % sensordict['humidity'])
   print("North: %s" % sensordict['compass'])


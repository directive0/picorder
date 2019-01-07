#!/usr/bin/python	

## This file fetches CPU load values and relates them to the caller. This file is used in place of the 

from __future__ import division
import copy
import math
import sys
import os
import psutil
import time

class led_display(object):
	def __init__(self):
		pass
		
	def toggle(self):
		pass
			

	# Function to draw a pretty pattern to the display.        
	def animate(self):
		pass
		
def translate(value, leftMin, leftMax, rightMin, rightMax):
	# Figure out how 'wide' each range is
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin

	# Convert the left range into a 0-1 range (float)
	valueScaled = float(value - leftMin) / float(leftSpan)

	# Convert the 0-1 range into a value in the right range.
	return rightMin + (valueScaled * rightSpan)


def sensorget():
   statusram = psutil.virtual_memory()
   
   sensordict = {'humidity': 0, 'temp':0, 'humidtemp':0, 'pressuretemp':0,'pressure':0,'compass':0} 
   sensordict['humidity'] = psutil.cpu_percent()
   sensordict['temp'] = psutil.sensors_temperatures()['acpitz'][0].current
   sensordict['humidtemp'] = psutil.cpu_percent()
   sensordict['pressuretemp'] = psutil.cpu_percent()
   sensordict['pressure'] = translate(statusram.percent, 0, 100, 260, 1260)
   #psutil.disk_usage('/').percent + 260
   sensordict['compass'] = {"x" : 2, "y" : 2, "z" : 3}
   return sensordict

def printscreen(sensordict):
   print("Temperature: %s C" % sensordict['temp'])
   print("Temperature from humidity: %s C" % sensordict['humidtemp'])
   print("Temperature from pressure: %s C" % sensordict['pressuretemp'])
   print("Pressure: %s Millibars" % sensordict['pressure'])
   print("Humidity: %s %%rH" % sensordict['humidity'])
   print("North: %s" % sensordict['compass'])


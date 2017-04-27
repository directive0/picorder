# External module imports
import RPi.GPIO as GPIO
import pygame
import sys
import time

# Pin Definitons:
led1 = 4 # Broadcom pin 4 (Pi0 pin 7)
led2 = 17 # Broadcom pin 17 (Pi0 pin 11)
led3 = 27 # Broadcom pin 27 (P1 pin 13)

buta = 5
butb = 6
butc = 13


# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(led1, GPIO.OUT) # LED pin set as output
GPIO.setup(led2, GPIO.OUT) # LED pin set as output
GPIO.setup(led3, GPIO.OUT) # LED pin set as output
GPIO.setup(buta, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Circle Button for GPIO23
GPIO.setup(butb, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Square Button for GPIO22
GPIO.setup(butc, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #R Button for GPIO4


def cleangpio():
    GPIO.cleanup() # cleanup all GPIO

def resetleds():
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)
    GPIO.output(led3, GPIO.LOW)


def leda_on():
    GPIO.output(led1, GPIO.HIGH)
    
def ledb_on():
    GPIO.output(led2, GPIO.HIGH)
    
def ledc_on():
    GPIO.output(led3, GPIO.HIGH)

def leda_off():
    GPIO.output(led1, GPIO.LOW)
    
def ledb_off():
    GPIO.output(led2, GPIO.LOW)

def ledc_off():
    GPIO.output(led3, GPIO.LOW)

def cycleloop():
	while True:
    		try:
			leda_on()
    			time.sleep(0.2)
			leda_off()
    			time.sleep(0.2)
			ledb_on()
    			time.sleep(0.2)
			ledb_off()
    			time.sleep(0.2)
			ledc_on()
    			time.sleep(0.2)
			ledc_off()
    			time.sleep(0.2)
    		except KeyboardInterrupt:
			print("cleaning up")
			
			cleangpio()
        		print("shutting down")
			sys.exit()


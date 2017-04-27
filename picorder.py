#!/usr/bin/python
# Picorder - Version 1.0
# Program collects sensor data and displays it to 4 bar graphs
# Uses interval timers to direct flow of program
# todo: 
# - Add GPIO lights and microswitches
# - Add OMXplayer support for "Edith Keeler" mode


# The following are some necessary modules for the Picorder.
import pygame
import os
import time
import random
from gpiobasics import *

#switch between gathering Sense-Hat sensor data or Open Weather Map data (requires internet).

#uncomment next line for Sense-Hat
from sensehatbasics import *

#uncomment next line for Sense-Hat
#from getweather import *

pygame.init()
pygame.font.init()
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.mouse.set_visible(0)

red = (255,0,0)
green = (106,255,69)
blue = (99,157,255)
black = (0,0,0)
white = (255,255,255)
yellow = (255,221,5)
titleFont = "babs.otf"
contentFont = "pixel.ttf"
blueInsignia = pygame.image.load('insigniablue.png')
backplane = pygame.image.load('background.png')
slider = pygame.image.load('slider.png')
status = "startup"


# The following class is used to display text
class Label(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = white
        self.fontSize = 33
        self.myfont = pygame.font.Font(titleFont, self.fontSize)
        
    def update(self, content, fontSize, nx, ny, fontType, color):
        self.x = nx
        self.y = ny
        self.content = content
        self.fontSize = fontSize
        self.myfont = pygame.font.Font(fontType, self.fontSize)
        self.color = color
        
    def draw(self, surface):
        label = self.myfont.render(self.content, 1, self.color)
        surface.blit(label, (self.x, self.y))

# the following class is used to display images
class Image(object):
    def __init__(self):
        self.x = 258
        self.y = 66
        self.Img = blueInsignia
        
    def update(self, image, nx, ny):
        self.x = nx
        self.y = ny
        self.Img = image

        
    def draw(self, surface):
        surface.blit(self.Img, (self.x,self.y))
        
        
# the following class is used to draw rectangles   
class Box(object):
    def __init__(self):
        self.x=0
        self.y=0
        self.vx=1
        self.vy=1
        self.size=(50,50)
        self.color=(0,0,255)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x > 640:
            self.vx = -1
            
        if self.x < 0:
            self.vx = 1
            
    
        if self.y > 480:
            self.vy = -1
        
        if self.y < 0:
            self.vy = 1
    
    def draw(self, surface):
        rect = pygame.Rect((self.x,self.y), self.size)
        pygame.draw.rect(surface, self.color, rect)


# the following class is used to make items flash by providing a timed pulse bit within the global scope  
class flash(object):
    def __init__(self):
     self.value = 0
     self.timelast = 0
     self.timenow = 0

    def pulse(self):
        
     if (self.timelast == 0):
         self.timelast = time.time()
        
     self.timenow = time.time() 
     
     if ((self.timenow - self.timelast) >= 1):
   
         if (self.value == 1):
             self.value = 0
         else:
             self.value = 1
     
         self.timelast = time.time()
            
    def display(self):
     return self.value     
     
class graphlist(object):
    
    def __init__(self):
        self.glist = []
        for i in range(300):
            self.glist.append(0)
    
    def grablist(self):
        return self.glist
        
    def updatelist(self,listin):
        self.glist = listin
    

# the following function maps a value from the target range onto the desination range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def rotate(lst, x):
    if x >= 0:
        for i in range(x):
            lastNum = lst.pop(-1)
            lst.insert(0, lastNum)

    else:
        for i in range(abs(x)):
            firstNum = lst.pop(0)
            lst.append(firstNum)

    return


    
def floatstrip(x):
    if x == int(x):
        return str(int(x))
    else:
        return str(x)    
    

# the following function runs the startup animation
def startUp(surface, timeSinceStart):
    #This function draws the opening splash screen for the program that provides the user with basic information.
    
    #Sets a black screen ready for our UI elements
    surface.fill(black)
    
    #Instantiates the components of the scene    
    insignia = Image()  
    mainTitle = Label()
    secTitle = Label()
    
    #sets out UI objects with the appropriate data
    insignia.update(blueInsignia, 115, 24) 
    mainTitle.update("TR-100 Environmental Tricorder",27,12,181,titleFont,yellow)
    secTitle.update("STARFLEET R&D - Toronto - CLASS M ONLY",19,37,210,titleFont,red)

    #writes our objects to the buffer
    insignia.draw(surface)
    
    #checks time   
    timenow = time.time()   
    
    #compares time just taken with time of start to animate the apperance of text
    if (timenow - timeSinceStart) > .5:
     mainTitle.draw(surface)
     
    if (timenow - timeSinceStart) > 1:
     secTitle.draw(surface)
    
    pygame.display.flip()

    #waits for 2 seconds to elapse before returning the state that will take us to the sensor readout
    if (timenow - timeSinceStart) < 2.5:
     return "startup"
    else:
     return "slidergo"

# the following function draws the main sensor readout screen
def sliderScreen(surface,moire):
      # This function draws the main 3-slider interface, modelled after McCoy's tricorder in "Plato's Stepchildren". It displays temperature, humidity and pressure.
      #Sets a black screen ready for our UI elements
      surface.fill(black)
      
      moire.animate()
      #Instantiates the components of the scene
      templabel = Label()
      presslabel = Label()
      humidlabel = Label()    
      backPlane = Image()  
      slider1 = Image()
      slider2 = Image()    
      slider3 = Image()
     
      #Grabs data from our sensor/weather package (depends on what module is imported at the top)
      senseData = sensorget()
     
      #parses dictionary of data from sensor/weather
      tempData = str(int(senseData['temp']))
      pressData = str(int(senseData['pressure']))
      humidData = str(int(senseData['humidity']))
      
      
      #data labels
      templabel.update(tempData + "\xb0",19,47,215,titleFont,yellow)
      presslabel.update(pressData,19,152,215,titleFont,yellow)
      humidlabel.update(humidData,19,254,215,titleFont,yellow)
      
      #slider data adjustment
      tempslide = translate(senseData['temp'], -40, 120, 200, 2)
      pressslide = translate(senseData['pressure'], 260, 1260, 200, 2)
      humidslide = translate(senseData['humidity'], 0, 100, 200, 2)

      #Updates our UI objects with data parsed from sensor/weather
      backPlane.update(backplane, 0, 0) 
      slider1.update(slider, 70, tempslide)
      slider2.update(slider, 172, pressslide)  
      slider3.update(slider, 276, humidslide)
      
      #draws the graphic UI to the buffer
      backPlane.draw(surface)
      slider1.draw(surface)
      slider2.draw(surface)
      slider3.draw(surface)

      #draws the labels to the buffer
      templabel.draw(surface)
      presslabel.draw(surface)
      humidlabel.draw(surface)

      #draws UI to frame buffer
      pygame.display.flip()
      
      #returns state to main loop
      return "slidergo"
    
#the following function plots the sensors to an onscreen graph (thats the plan, anyways for now this is stillborn)    
def graphScreen(surface):
    
      #Sets a black screen ready for our UI elements
      surface.fill(black)
      
      senseData = sensorget()
     
      #parses dictionary of data from sensor/weather
      tempData = str(int(senseData['temp']))
      tempgraph = translate(20, -40, 120, 210, 10)
      
      bufferlist = templist.grablist()
      
      bufferlist.append(tempgraph)
      bufferlist.pop(0)
      
      graph = pygame.PixelArray(surface)
              
      for x in range(10, 309):
          stats = 0
          for y in range(10,210):
              if (y == bufferlist[stats]): 
               graph[x,y]= (255,0,0)
               stats = stats + 1

      
      #Instantiates the components of the scene

     
      #Grabs data from our sensor/weather package (depends on what module is imported at the top)
      #senseData = sensorget()
     
      #parses dictionary of data from sensor/weathe
      
      
      #data labels

      #slider data adjustment

      #Updates our UI objects with data parsed from sensor/weather

      
      #draws the graphic UI to the buffer

      #draws the labels to the buffer

      #draws UI to frame buffer
      pygame.display.flip()
      
      #returns state to main loop
      return "slidergo"
    

 
# the following function is our main object, it contains all the flow for our program
class Main(object):
    
    # set the screen resolution
    screenSize = (320,240)
    
    # I forget
    modes = pygame.display.list_modes(16)

    # instantiate a pygame display with the name "surface"
    surface = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)

    # Create a time index to work from for the splash screen.
    timeSinceStart = time.time()
    
    while(status == "startup"):
        pygame.time.wait(33)
        pygame.event.get()  
        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            status = quit
        else:
            #timeStart=time.time()
            status = startUp(surface,timeSinceStart)


    moire = led_display()
    
    while(status == "slidergo"):

        pygame.event.get()
        pygame.time.wait(33)
        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            status = quit
        else:
            #timeStart=time.time()
            status = sliderScreen(surface,moire)

    
    cleangpio()
        
    
         
# the following call starts our program         
Main()

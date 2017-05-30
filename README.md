# The TR-108 Picorder
The following is a set of python programs that provide functionality for the TR-108 Tricorder I am building, as well as necessary files for anyone to build their own should they so desire

## Requirements:
Picorder.py uses a number of modules to operate, specifically:
- Pygame
- Senshat
- RPi.GPIO
- sys
- time
- math
- os
- psutil (PC Demo only)

Be sure you have these modules installed before attempting to run this program.

## Notes:
Basic functionality is complete; the program logs values from the sense hat and displays them. Future releases will optimize this code, for now its a dogs breakfast. What do you expect, I'm a noob.

## Construction:
You can find all the necessary construction documents in the "construction" folder.

Adafruit parts Wishlist is here:
http://www.adafruit.com/wishlists/435166

The base I used for the tricorder:
https://www.amazon.ca/gp/product/B001820194/ref=ox_sc_sfl_title_6?ie=UTF8&psc=1&smid=A3DWYIK6Y9EEQB

## Sources
This project was made possible by information and inspiration provided by these sources:
- https://hackaday.io/project/5437-star-trek-tos-picorder
- https://github.com/tobykurien/rpi_lcars

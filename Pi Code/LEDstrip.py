import time
import os
import RPi.GPIO as GPIO
import sys
import math
sys.path.insert(0, '/home/pi/.local/lib/python3.5/site-packages')
import board
sys.path.insert(0, '/usr/local/lib/python3.5/dist-packages')
import neopixel

GPIO.setmode(GPIO.BCM)

# Assigns Pins for ADC
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# Assigns for LED strip
pixel_number = 300
pin_number = board.D18
light_delay = 0.00001

# Lists for LED strip
pixel_list = []
bounceback_list = []

# Assigns pixels to LEDs
pixels = neopixel.NeoPixel(pin_number, pixel_number, brightness=0.1, auto_write=False, pixel_order=neopixel.GRB)

# Reads ADC voltage (Based on Adafruit's ADC python code)
def readadc(adcpin, clockpin, mosipin, misopin, cspin):
    if((adcpin < 0) or (adcpin > 7)):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)

    commandout = adcpin
    commandout |= 0x18
    commandout <<= 3
    for i in range(5):
        if(commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0

    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if(GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1
    adcout = adcout * 3.3 / 1023
    return adcout

# Changes color of LEDs to blue, purple, white based off voltages
def volt_color(volt):
    volt = volt * 765 / 3.3
    if volt <= 255:
        return (0,0,math.floor(volt))
    elif (volt > 255) and (volt <= 509):
        return (math.floor(volt - 255),0,255)
    elif (volt > 510) and (volt <= 764):
        return (255,math.floor(volt - 510),255)
    else:
        return (255,255,255)

# Changes color of LEDs to a multitude of colors based off voltages
def volt_color_advanced(volt):
    volt = volt * 1375 / 3.3
    if volt <= 255:
        return (math.floor(volt * 31 / 255),math.floor(volt),math.floor(volt))
    elif (volt > 255) and (volt <= 479):
        return (31,255-math.floor(volt - 255),255)
    elif (volt > 479) and (volt <= 703):
        return (31 + math.floor(volt - 479),31,255)
    elif (volt > 703) and (volt <= 927):
        return (255,31,255 - math.floor(volt - 703))
    elif (volt > 927) and (volt <= 1151):
        return (255,31 + math.floor(volt - 927),31)
    elif (volt > 1151) and (volt <= 1375):
        return (255,255,31 + math.floor(volt - 1151))
    else:
        return (255,255,255)

# Sends rainbow colors down the LED strip
def rainbow_run(delay):
    continuous_run('r')
    time.sleep(delay)
    continuous_run('o')
    time.sleep(delay)
    continuous_run('y')
    time.sleep(delay)
    continuous_run('g')
    time.sleep(delay)
    continuous_run('t')
    time.sleep(delay)
    continuous_run('b')
    time.sleep(delay)
    continuous_run('v')
    time.sleep(delay)
    continuous_run('p')
    time.sleep(delay)

# Sends rainbow colors down and back on LED strip
def rainbow_bounceback(delay):
    bounceback_run('r')
    time.sleep(delay)
    bounceback_run('o')
    time.sleep(delay)
    bounceback_run('y')
    time.sleep(delay)
    bounceback_run('g')
    time.sleep(delay)
    bounceback_run('t')
    time.sleep(delay)
    bounceback_run('b')
    time.sleep(delay)
    bounceback_run('v')
    time.sleep(delay)
    bounceback_run('p')
    time.sleep(delay)

# Changes through colors while increasing and decreasing brightness
def rainbow_flash(delay):
    stillChanging = True
    loopDone = False
    incBright = True
    r = 0
    g = 0
    b = 255
    bright = 0.05
    colorChanger = 0
    while stillChanging:
        if incBright:
            bright += 0.01
            if bright > 0.95:
                incBright = False
        else:
            bright -= 0.01
            if bright < 0.05:
                incBright = True
        if colorChanger == 0:
            r = r + 1
            if r >= 254:
                colorChanger += 1
        elif colorChanger == 1:
            b = b - 1
            if b <= 1:
                colorChanger += 1
        elif colorChanger == 2:
            g = g + 1
            if g >= 254:
                colorChanger += 1
        elif colorChanger == 3:
            r = r - 1
            if r <= 1:
                colorChanger += 1
        elif colorChanger == 4:
            b = b + 1
            if b >= 254:
                colorChanger += 1
        elif colorChanger == 5:
            g = g - 1
            if loopDone == True:
                stillChanging = False
            elif g <= 1:
                colorChanger = 0
                loopDone = True
        else:
            print("Something is not right")
        pixels.fill((r,g,b))
        pixels._brightness = bright
        pixels.show()
        time.sleep(delay)

# Sends a color down the LED strip 
def light_run(color):
    for i in range(pixel_number):
        color = hex_color(color)
        pixels[i] = color
        if i > 0:
            pixels[i - 1] = (0,0,0)
        pixels.show()
        time.sleep(0.01)

# Converts colors to their hex values
def hex_color(color):
    if color == 'r':
        return (255,0,0)
    elif color == 'o':
        return (255,108,0)
    elif color == 'y':
        return (255,249,46)
    elif color == 'g':
        return (50,255,0)
    elif color == 't':
        return (0,244,244)
    elif color == 'b':
        return (0,0,255)
    elif color == 'v':
        return (107,0,244)
    elif color == 'p':
        return (244,0,177)
    elif color == 'br':
        return (112,73,25)
    elif color == 'w':
        return (255,255,255)
    else:
        return (0,0,0)

# Sends a chain of colors down the LED and keeps sending them using a list
def continuous_run(color):
    color = hex_color(color)
    pixel_list.insert(0,color)
    if len(pixel_list) >= pixel_number:
        pixel_list.pop()
    for i in range(len(pixel_list)):
        pixels[len(pixel_list) - i - 1] = pixel_list[len(pixel_list) - i - 1]
    pixels.show()

# Sends a chain of colors down the LED and then runs back using a list
def bounceback_run(color):
    color = hex_color(color)
    bounceback_list.insert(0,color)
    if len(bounceback_list) >= pixel_number:
        for i in range(pixel_number):
            del bounceback_list[0]
            for j in range(pixel_number):
                if j < len(bounceback_list):
                    pixels[j] = bounceback_list[j]
                if j >= len(bounceback_list):
                    pixels[j] = (0,0,0)
            pixels.show()
    if len(bounceback_list) < pixel_number:
        for i in range(len(bounceback_list)):
            pixels[len(bounceback_list) - i - 1] = bounceback_list[len(bounceback_list) - i - 1]
        pixels.show()    

# clears the LED strip
def clear():
    pixels.fill((0,0,0))
    pixels.show()

# Resets the LED strip
clear()
time.sleep(1)

# Sets up the GPIO pins for SPI communication with the ADC
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Constantly reads in the ADC voltage and 
# then converts it to a color to be displayed.
# The higher the frequency and volume, the brighter the colors
while True:
    fvolt = readadc(1,SPICLK,SPIMOSI,SPIMISO,SPICS)
    pixels.fill(volt_color_advanced(fvolt))
    pixels._brightness = fvolt / 5
    pixels.show()

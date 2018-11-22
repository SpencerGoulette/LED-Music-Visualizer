import time
import sys
sys.path.insert(0, '/home/pi/.local/lib/python3.5/site-packages')
import board
sys.path.insert(0, '/usr/local/lib/python3.5/dist-packages')
import neopixel

pixel_number = 300
pin_number = board.D18
light_delay = 0.00001

pixel_list = []
bounceback_list = []

pixels = neopixel.NeoPixel(pin_number, pixel_number, brightness=0.1, auto_write=False, pixel_order=neopixel.GRB)

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


def rainbow_flash(delay):
    stillChanging = True
    loopDone = False
    r = 0
    g = 0
    b = 255
    colorChanger = 0
    while stillChanging:
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
        time.sleep(delay)

def light_run(color):
    for i in range(pixel_number):
        color = hex_color(color)
        pixels[i] = color
        if i > 0:
            pixels[i - 1] = (0,0,0)
        pixels.show()
        time.sleep(0.01)

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

def continuous_run(color):
    color = hex_color(color)
    pixel_list.insert(0,color)
    if len(pixel_list) >= pixel_number:
        pixel_list.pop()
    for i in range(len(pixel_list)):
        pixels[len(pixel_list) - i - 1] = pixel_list[len(pixel_list) - i - 1]
    pixels.show()

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
        

def clear():
    pixels.fill((0,0,0))
    pixels.show()

clear()
while True:
    rainbow_bounceback(light_delay)


import time
import sys
sys.path.insert(0, '/home/pi/.local/lib/python3.5/site-packages')
import board
sys.path.insert(0, '/usr/local/lib/python3.5/dist-packages')
import neopixel

pixel_number = 255
pin_number = board.D18
light_delay = 0.00001

pixels = neopixel.NeoPixel(pin_number, pixel_number)

def rainbow_run(delay):
    for i in range(0,8):
        for j in range(pixel_number):
            change = i*31;
            pixels[j] = (change,0,255-change)
            pixels.show()
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
        if color == 'r':
            pixels[i] = (255,0,0)
        elif color == 'o':
            pixels[i] = (255,125,0)
        elif color == 'y':
            pixels[i] = (255,233,0)
        elif color == 'g':
            pixels[i] = (50,255,0)
        elif color == 't':
            pixels[i] = (0,244,244)
        elif color == 'b':
            pixels[i] = (0,0,255)
        elif color == 'v':
            pixels[i] = (107,0,244)
        elif color == 'p':
            pixels[i] = (244,0,177)
        if i > 0:
            pixels[i - 1] = (0,0,0) 
        time.sleep(0.01)

def clear():
    pixels.fill((0,0,0))

while True:
    clear()
    time.sleep(10)
    light_run('r')
    light_run('o')
    light_run('y')
    light_run('g')
    light_run('t')
    light_run('b')
    light_run('v')
    light_run('p')
    time.sleep(1)
    rainbow_flash(light_delay)
    time.sleep(1)


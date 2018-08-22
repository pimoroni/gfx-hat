#!/usr/bin/env python

import time
import sys
import atexit
from gfxhat import lcd, backlight, touch, fonts
from PIL import Image, ImageDraw, ImageFont
import yaml

print("""upinout.py

Micro Pinout! A tiny version of Pinout.xyz.

Ever wondered what your GPIO pins do? What their BCM/WiringPi numbers are?

Use - and + to navigate the header and find out!

To see alt modes, use ^ and v on the left.

Press Ctrl + C to exit.

""")

pinout = yaml.load(open("pinout.yaml").read())
src = Image.open("upinout.png").convert("P")

width, height = lcd.dimensions()

font = ImageFont.truetype(fonts.BitocraFull, 11)

current_pin = 0
current_page = 0
running = True

backlight.set_all(255, 255, 255)
backlight.show()

def handle_input(ch, evt):
    global current_pin, current_page, running

    if evt == 'press':
        if ch == touch.MINUS:
            current_page = 0
            current_pin -= 1
            current_pin %= 40

        if ch == touch.PLUS:
            current_page = 0
            current_pin += 1
            current_pin %= 40

        if ch == touch.BACK:
            running = False

        pin_details = pinout['pins'][str(current_pin+1)]

        page_size = 1

        if 'functions' in pin_details:
            page_size = 3

        if ch == touch.UP:
            current_page -= 1
            current_page %= page_size

        if ch == touch.DOWN:
            current_page += 1
            current_page %= page_size

def draw_cursor(image, x, y, direction):
    y = y if direction else y + 2

    image.putpixel((x + 2, y), 1)

    y = y + 1 if direction else y - 1
    for p in range(3):
        image.putpixel((x + 1 + p, y), 1)

    y = y + 1 if direction else y - 1
    for p in range(5):
        image.putpixel((x + p, y), 1)

for x in range(6):
    touch.on(x, handle_input)

def clear():
    lcd.clear()
    lcd.show()
    backlight.set_all(0, 0, 0)
    backlight.show()

atexit.register(clear)

while running:
    img = src.copy()
    draw = ImageDraw.Draw(img)

    if (current_pin + 1) % 2 == 0:
        offset_x = ((current_pin + 1) // 2) * 6
        offset_y = 9
        direction = 0
    else:
        offset_x = ((current_pin + 2) // 2) * 6
        offset_y = 25
        direction = 1

    draw_cursor(img, offset_x - 2, offset_y, direction)

    pin_details = pinout['pins'][str(current_pin+1)]

    if current_page == 0:
        name = ''

        if 'name' in pin_details:
            name = pin_details['name'].strip()
            if len(name) > 0:
                name += ' '
        
        draw.text((4, 34), "{}#{}".format(name, current_pin + 1), 1, font)

        if 'scheme' in pin_details:
            if 'bcm' in pin_details['scheme']:
                bcm = pin_details['scheme']['bcm']
                draw.text((4, 42), "BCM: #{}".format(bcm), 1, font)
            if 'wiringpi' in pin_details['scheme']:
                wiringpi = pin_details['scheme']['wiringpi']
                draw.text((4, 50), "WiringPi: #{}".format(wiringpi), 1, font)

    if current_page == 1:
        if 'functions' in pin_details:
            functions = pin_details['functions']
            alt_y = 0
            for alt in ['alt0', 'alt1', 'alt2']:
                if alt not in functions: continue
                name = functions[alt]
                draw.text((4, 34 + alt_y), "{}: {}".format(alt, name), 1, font)
                alt_y += 8

    if current_page == 2:
        if 'functions' in pin_details:
            functions = pin_details['functions']
            alt_y = 0
            for alt in ['alt3', 'alt4']:
                if alt not in functions: continue
                name = functions[alt]
                draw.text((4, 34 + alt_y), "{}: {}".format(alt, name), 1, font)
                alt_y += 8

    if 'functions' in pin_details:
        scroll_y = 33 + (current_page * 10)
        draw.rectangle(((124, scroll_y),(126, scroll_y + 10)), 1) 

    backlight.set_all(255, 255, 255)

    if 'type' in pin_details:
        pin_type = pin_details['type']
        if pin_type == 'GPIO/I2C':
            backlight.set_all(255, 0, 255)
        if pin_type == 'GPIO/SPI':
            backlight.set_all(0, 0, 255)
        if pin_type == 'GND':
            backlight.set_all(128, 128, 128)    
        if pin_type == '+5v':
            backlight.set_all(255, 0, 0)
        if pin_type == '+3v3':
            backlight.set_all(255, 255, 0)

    backlight.show()

    # Blit our image canvas to the LCD
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            lcd.set_pixel(x, y, pixel)

    lcd.show()
    time.sleep(1 / 30.0)


#!/usr/bin/env python

from gfxhat import lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw
import time

print("""

GFX HAT - Contrast Scanner

This example scans through the available contrast values, from 20 to 63,
and displays this on the LCD. This is then repeated with the backlight
set to white.

Contrast values below around 20 are not visible and are skipped.

Press Ctrl+C to exit.

""")

font = ImageFont.truetype(fonts.Bitocra13Full, 13)

width, height = lcd.dimensions()

image = Image.new("1", (128, 64), "black")
draw = ImageDraw.Draw(image)


def scan_contrast():
    for c in range(25, 64):
        draw.rectangle((0, 0, width, height), "black")

        message = "Contrast: {:02d}".format(c)

        w, h = font.getsize(message)
        left, top = (width - w) / 2, (height - h) / 2

        draw.text((left, top), message, 1, font=font)

        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))
                lcd.set_pixel(x, y, pixel)

        lcd.contrast(c)
        lcd.show()
        time.sleep(0.4)

    lcd.clear()
    lcd.show()


lcd.show()

backlight.set_all(0, 0, 0)
backlight.show()


try:
    lcd.contrast(0)
    scan_contrast()

    lcd.contrast(0)
    backlight.set_all(255, 255, 255)
    backlight.show()

    scan_contrast()
    lcd.contrast(0)

    backlight.set_all(0, 0, 0)
    backlight.show()
    print("Done!")

except KeyboardInterrupt:
    lcd.contrast(0)
    backlight.set_all(0, 0, 0)
    backlight.show()
    print("Quit via keyboard.")

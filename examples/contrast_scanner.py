#!/usr/bin/python3

from gfxhat import lcd, backlight
from PIL import Image, ImageFont, ImageDraw
import time

print("""contrast_scanner.py

This example scans through the available contrast values, from 0-63,
and displays this on the LCD. This is then repeated with the backlight
set to white. You won't see anything for about 20 seconds each time 
because values below around 25 aren't visible.

Press Ctrl+C to exit.

""")

lm = ImageFont.truetype("/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf", 16)
lm_big =  ImageFont.truetype("/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf", 56)


lcd.show()

backlight.set_all(0,0,0)
backlight.show()


def scan_contrast():
	for c in range (0,64):
		im = Image.new("1", (128,64), "black")
		im2 = ImageDraw.Draw(im)

		im2.text((19,0), "Contrast: ", 1, font=lm)

		position = lm_big.getsize(str(c))
		im2.text((64 - (position[0]/2), 10), str(c), 1, font=lm_big)
		for x in range (128):
			for y in range (64):
				pixel = im.getpixel((x,y))
				lcd.set_pixel(x, y, pixel)
		lcd.contrast(c)
		lcd.show()
		time.sleep(0.5)
	lcd.clear()
	lcd.show()

try:
	lcd.contrast(0)
	scan_contrast()

	lcd.contrast(0)
	backlight.set_all(255,255,255)
	backlight.show()

	scan_contrast()
	lcd.contrast(0)

	backlight.set_all(0,0,0)
	backlight.show()
	print("Done!")
except KeyboardInterrupt:
	lcd.contrast(0)
	backlight.set_all(0,0,0)
	backlight.show()
	print("Quit via keyboard.")

_sn3218 = None

_buf = [0 for x in range(18)]

LED_MAP = [2, 1, 0, 5, 4, 3]

def setup():
    global _sn3218
    import sn3218 as _sn3218

    _sn3218.enable()
    _sn3218.enable_leds(0b111111111111111111)
    _sn3218.output(_buf)

def set_pixel(x, r, g, b):
    global _buf
    if x > 5 or x < 0:
        raise ValueError("x should be in the range 0 to 5")

    x = LED_MAP[x]
    x *= 3
    _buf[x:x+3] = b, g, r

def show():
    setup()
    _sn3218.output(_buf)

if __name__ == "__main__":
    import time
    import colorsys

    def wipe(r, g, b):
        for x in range(6):
            set_pixel(x, r, g, b)
            show()
            time.sleep(0.1)
            set_pixel(x, 0, 0, 0)

    wipe(255, 0, 0)
    wipe(0, 255, 0)
    wipe(0, 0, 255)
    wipe(0, 0, 0)

    try:
        while True:
            t = time.time()
            for x in range(6):
                offset = (t * 250) + (x * 30)
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(offset / 360.0, 1.0, 1.0)]
                g = int(g * 0.8)
                b = int(b * 0.8)
                set_pixel(x, r, g, b)
            show()
            time.sleep(1.0 / 60)
    except KeyboardInterrupt:
        pass


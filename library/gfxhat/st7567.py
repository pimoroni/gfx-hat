import RPi.GPIO as GPIO
import spidev
import time
import random

SPI_SPEED_HZ = 1000000

WIDTH = 128
HEIGHT = 64

PIN_CS = 8
PIN_RST = 5
PIN_DC = 6

ST7567_PAGESIZE = 128

ST7567_DISPOFF = 0xae         # 0xae: Display OFF (sleep mode) */
ST7567_DISPON = 0xaf          # 0xaf: Display ON in normal mode */

ST7567_SETSTARTLINE = 0x40    # 0x40-7f: Set display start line */
ST7567_STARTLINE_MASK = 0x3f

ST7567_REG_RATIO = 0x20

ST7567_SETPAGESTART = 0xb0    # 0xb0-b7: Set page start address */
ST7567_PAGESTART_MASK = 0x07

ST7567_SETCOLL = 0x00         # 0x00-0x0f: Set lower column address */
ST7567_COLL_MASK = 0x0f
ST7567_SETCOLH = 0x10         # 0x10-0x1f: Set higher column address */
ST7567_COLH_MASK = 0x0f

ST7567_SEG_DIR_NORMAL = 0xa0  # 0xa0: Column address 0 is mapped to SEG0 */
ST7567_SEG_DIR_REV = 0xa1     # 0xa1: Column address 128 is mapped to SEG0 */

ST7567_DISPNORMAL = 0xa6      # 0xa6: Normal display */
ST7567_DISPINVERSE = 0xa7     # 0xa7: Inverse display */

ST7567_DISPRAM = 0xa4         # 0xa4: Resume to RAM content display */
ST7567_DISPENTIRE = 0xa5      # 0xa5: Entire display ON */

ST7567_BIAS_1_9 = 0xa2        # 0xa2: Select BIAS setting 1/9 */
ST7567_BIAS_1_7 = 0xa3        # 0xa3: Select BIAS setting 1/7 */

ST7567_ENTER_RMWMODE = 0xe0   # 0xe0: Enter the Read Modify Write mode */
ST7567_EXIT_RMWMODE = 0xee    # 0xee: Leave the Read Modify Write mode */
ST7567_EXIT_SOFTRST = 0xe2    # 0xe2: Software RESET */

ST7567_SETCOMNORMAL = 0xc0    # 0xc0: Set COM output direction, normal mode */
ST7567_SETCOMREVERSE = 0xc8   # 0xc8: Set COM output direction, reverse mode */

ST7567_POWERCTRL_VF = 0x29    # 0x29: Control built-in power circuit */
ST7567_POWERCTRL_VR = 0x2a    # 0x2a: Control built-in power circuit */
ST7567_POWERCTRL_VB = 0x2c    # 0x2c: Control built-in power circuit */
ST7567_POWERCTRL = 0x2f       # 0x2c: Control built-in power circuit */

ST7567_REG_RES_RR0 = 0x21     # 0x21: Regulation Resistior ratio */
ST7567_REG_RES_RR1 = 0x22     # 0x22: Regulation Resistior ratio */
ST7567_REG_RES_RR2 = 0x24     # 0x24: Regulation Resistior ratio */

ST7567_SETCONTRAST = 0x81     # 0x81: Set contrast control */

ST7567_SETBOOSTER = 0xf8      # Set booster level */
ST7567_SETBOOSTER4X = 0x00    # Set booster level */
ST7567_SETBOOSTER5X = 0x01    # Set booster level */

ST7567_NOP = 0xe3             # 0xe3: NOP Command for no operation */

ST7565_STARTBYTES = 0


class ST7567:
    def __init__(self, pin_rst=PIN_RST, pin_dc=PIN_DC, spi_bus=0, spi_cs=0, spi_speed=SPI_SPEED_HZ):
        self._is_setup = False
        self.pin_rst = pin_rst
        self.pin_dc = pin_dc
        self.spi_bus = spi_bus
        self.spi_cs = spi_cs
        self.spi_speed = spi_speed
        self.clear()

    def setup(self):
        if self._is_setup:
            return True

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_rst, GPIO.OUT)
        GPIO.setup(self.pin_dc, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(self.spi_bus, self.spi_cs)
        self.spi.max_speed_hz = self.spi_speed

        self._reset()
        self._init()

        self._is_setup = True

    def dimensions(self):
        return (WIDTH, HEIGHT)

    def clear(self):
        self.buf = [0 for _ in range(128*64//8)]

    def _command(self, data):
        GPIO.output(self.pin_dc, 0)
        self.spi.writebytes(data)

    def _data(self, data):
        GPIO.output(self.pin_dc, 1)
        self.spi.writebytes(data)

    def _reset(self):
        GPIO.output(self.pin_rst, 0)
        time.sleep(0.01)
        GPIO.output(self.pin_rst, 1)
        time.sleep(0.1)

    def _init(self):
        self._command([
            ST7567_BIAS_1_7,          # Bais 1/7 (0xA2 = Bias 1/9)
            ST7567_SEG_DIR_NORMAL,
            ST7567_SETCOMREVERSE,     # Reverse COM - vertical flip
            ST7567_DISPNORMAL,        # Inverse display (0xA6 normal)
            ST7567_SETSTARTLINE | 0,  # Start at line 0
            ST7567_POWERCTRL,
            ST7567_REG_RATIO | 2,
            ST7567_DISPON,
            ST7567_SETCONTRAST,       # Set contrast
            58                        # Contrast value
        ])

    def set_pixel(self, x, y, value):
        offset = ((y//8) * WIDTH) + x
        bit = y % 8
        self.buf[offset] &= ~(1 << bit)
        self.buf[offset] |= (value & 1) << bit

    def show(self):
        self.setup()
        self._command([ST7567_ENTER_RMWMODE])
        for page in range(8):
            offset = page * ST7567_PAGESIZE
            self._command([ST7567_SETPAGESTART | page, ST7567_SETCOLL, ST7567_SETCOLH])
            self._data(self.buf[offset:offset+ST7567_PAGESIZE])
        self._command([ST7567_EXIT_RMWMODE])


if __name__ == "__main__":
    st7567 = ST7567()
    st7567.setup()

    for x in range(64):
        st7567.set_pixel(x, x, 1)
        st7567.set_pixel(64-x, x, 1)
        st7567.set_pixel(x+2, x, 1)
    st7567.show()

    time.sleep(2.0)

    try:
        while True:
            for x in range(128):
                for y in range(64):
                    st7567.set_pixel(x, y, random.randint(0, 1))
            st7567.show()
    except KeyboardInterrupt:
        pass

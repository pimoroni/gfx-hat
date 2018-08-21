import cap1xxx

_cap1166 = None
is_setup = False

I2C_ADDR = 0x2c

UP = 0
DOWN = 1
BACK = 2
MINUS = 3
SELECT = 4
PLUS = 5

LED_MAPPING = [5, 4, 3, 2, 1, 0]

def setup():
    global _cap1166, is_setup

    _cap1166 = cap1xxx.Cap1166(i2c_addr=I2C_ADDR)

    for x in range(6):
        _cap1166.set_led_linking(x, 0)

    is_setup = True

def set_led(index, state):
    """Set LED state

    :param index: LED index
    :param state: LED state (1 = on, 0 = off)

    """
    setup()
    _cap1166.set_led_state(LED_MAPPING[index], state)

def high_sensitivity():
    """Switch to high sensitivity mode

    This predetermined high sensitivity mode is for using
    touch through 3mm perspex or similar materials.

    """

    _cap1166._write_byte(0x00, 0b11000000)
    _cap1166._write_byte(0x1f, 0b00000000)

def enable_repeat(enable):
    """Enable touch hold repeat

    If enable is true, repeat will be enabled. This will
    trigger new touch events at the set repeat_rate when
    a touch input is held.

    :param enable: enable/disable repeat: True/False

    """

    if enable:
        _cap1166.enable_repeat(0b11111111)
    else:
        _cap1166.enable_repeat(0b00000000)

def set_repeat_rate(rate):
    """Set hold repeat rate

    Repeat rate values are clamped to the nearest 35ms,
    values from 35 to 560 are valid.

    :param rate: time in ms from 35 to 560

    """

    _cap1166.set_repeat_rate(rate)

def on(buttons, handler=None):
    """Handle a press of one or more buttons

    Decorator. Use with @captouch.on(UP)
    
    :param buttons: List, or single instance of cap touch button constant
    :param bounce: Maintained for compatibility with Dot3k joystick, unused

    """
    buttons = buttons if isinstance(buttons, list) else [buttons]

    def register(handler):
        for button in buttons:
            _cap1166.on(channel=button, event='press', handler=handler)
            _cap1166.on(channel=button, event='held', handler=handler)

    if handler is not None:
        register(handler)
        return

    return register


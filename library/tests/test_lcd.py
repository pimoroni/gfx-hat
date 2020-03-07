# noqa D100
import mock
import pytest


def test_st7567_init(GPIO):
    """Test that the ST7567 initialises correctly."""
    from gfxhat import lcd

    lcd.st7567.setup()

    GPIO.setmode.assert_called_once_with(GPIO.BCM)
    GPIO.setup.assert_has_calls([
        mock.call(6, GPIO.OUT),
        mock.call(5, GPIO.OUT)
    ], any_order=True)


def test_st7567_rotate():
    """Test that the ST7567 rotate feature works."""
    from gfxhat import lcd

    lcd.rotation(0)
    lcd.set_pixel(0, 0, 1)
    assert lcd.get_rotation() == 0

    lcd.rotation(180)
    lcd.set_pixel(0, 0, 1)
    assert lcd.get_rotation() == 180

    with pytest.raises(ValueError):
        lcd.rotation(90)


def test_st7567_clear():
    """Test that clear doesn't explode."""
    from gfxhat import lcd

    lcd.clear()


def test_st7567_show(spidev):
    """Test that show tries to enter RMWMODE over SPI."""
    from gfxhat import lcd, st7567

    lcd.show()

    spidev.SpiDev().writebytes.assert_has_calls([
        mock.call([st7567.ST7567_ENTER_RMWMODE])
    ])


def test_st7567_contrast(spidev):
    """Test that set_contrast tries to write over SPI."""
    from gfxhat import lcd, st7567

    lcd.contrast(11)

    spidev.SpiDev().writebytes.assert_has_calls([
        mock.call([st7567.ST7567_SETCONTRAST, 11])
    ])


def test_st7567_dimensions(spidev):
    """Test that lcd.dimensions returns the constants defined in st7567."""
    from gfxhat import lcd, st7567

    assert lcd.dimensions() == (st7567.WIDTH, st7567.HEIGHT)

# noqa D100
import pytest


def test_backlight_setup(sn3218):
    """Test that backlight enables all SN3218 LEDs."""
    from gfxhat import backlight

    backlight.setup()

    sn3218.enable.assert_called_once()
    sn3218.enable_leds.assert_called_with(0b111111111111111111)
    sn3218.output.assert_called_with([0] * 18)


def test_backlight_set_pixel(sn3218):
    """Test that set_pixel sets the right buffer elements."""
    from gfxhat import backlight

    with pytest.raises(ValueError):
        backlight.set_pixel(9, 255, 255, 255)

    backlight.set_pixel(0, 255, 255, 255)

    # TODO we probably shouldn't use implementation details to test the API
    # but with the absence of a corresponding `get_pixel`...
    offset = backlight.LED_MAP[0] * 3
    assert backlight._buf[offset:offset + 3] == [255, 255, 255]


def test_set_all(sn3218):
    """Test that set_all does not explode."""
    from gfxhat import backlight

    backlight.set_all(64, 64, 64)


def test_show(sn3218):
    """Test that show calls sn3218.output()."""
    from gfxhat import backlight

    backlight.show()

    sn3218.output.assert_called_with(backlight._buf)

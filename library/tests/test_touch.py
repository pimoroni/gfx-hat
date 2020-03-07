# noqa D100
import mock


def test_touch_setup(cap1xxx):
    """Test that touch initialises Cap1166."""
    from gfxhat import touch

    touch.setup()

    cap1xxx.Cap1166.assert_called_with(i2c_addr=touch.I2C_ADDR)


def test_touch_names():
    """Test that get_name returns a sensible value."""
    from gfxhat import touch

    assert touch.get_name(0) == 'up'


def test_touch_set_led(cap1xxx):
    """Test that set_led calls Cap1166.set_led_state."""
    from gfxhat import touch

    touch.set_led(0, True)

    cap1xxx.Cap1166().set_led_state.assert_called_with(touch.LED_MAPPING[0], True)


def test_touch_high_sensitivity(cap1xxx):
    """Test that high sensitivity calls custom commands.

    Tests should be updated if/when this behaviour is formalised in Cap1xxx.

    """
    from gfxhat import touch

    touch.high_sensitivity()

    cap1xxx.Cap1166()._write_byte.assert_has_calls([
        mock.call(0x00, 0b11000000),
        mock.call(0x1f, 0b00000000)
    ])


def test_touch_repeat(cap1xxx):
    """Test that touch repeat calls Cap1166.enable_repeat()."""
    from gfxhat import touch

    touch.enable_repeat(True)
    cap1xxx.Cap1166().enable_repeat.assert_called_with(0b11111111)

    touch.enable_repeat(False)
    cap1xxx.Cap1166().enable_repeat.assert_called_with(0b00000000)


def test_touch_repeat_rate(cap1xxx):
    """Test that touch repeat rate calls Cap1166.set_repeat_rate()."""
    from gfxhat import touch

    touch.set_repeat_rate(35)
    cap1xxx.Cap1166().set_repeat_rate.assert_called_with(35)


def test_attach_handler(cap1xxx):
    """Test that both handler modes call Cap1166.on()."""
    from gfxhat import touch

    decorator = touch.on([1])

    def handler():
        pass

    decorator(handler)

    cap1xxx.Cap1166().on.assert_has_calls([
        mock.call(channel=1, event='press', handler=handler),
        mock.call(channel=1, event='release', handler=handler),
        mock.call(channel=1, event='held', handler=handler),
    ])

    touch.on([0], handler=handler)

    cap1xxx.Cap1166().on.assert_has_calls([
        mock.call(channel=0, event='press', handler=handler),
        mock.call(channel=0, event='release', handler=handler),
        mock.call(channel=0, event='held', handler=handler),
    ])

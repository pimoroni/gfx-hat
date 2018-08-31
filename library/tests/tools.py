class GPIO:
    BCM = 1
    OUT = 1
    IN = 1

    def __init__(self):
        self.pin_modes = {}
        self.pin_states = {}

    def output(self, pin, value):
        self.pin_states[pin] = value

    def setmode(self, mode):
        pass

    def setwarnings(self, mode):
        pass

    def setup(self, pin, mode):
        self.pin_modes[pin] = mode

#!/usr/bin/env python

import signal
from gfxhat import touch

print("""touch.py

This basic example shows you the channel/event values you can expect
when touching different buttons.

Press Ctrl+C to exit.

""")

def handler(channel, event):
    print("Got {} on channel {}".format(event, channel))
    
for x in range(6):
    touch.on(x, handler)

signal.pause()

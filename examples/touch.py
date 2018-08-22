#!/usr/bin/env python

import signal
from gfxhat import touch

def handler(channel, event):
    print("Got {} on channel {}".format(event, channel))
    
for x in range(6):
    touch.on(x, handler)

signal.pause()

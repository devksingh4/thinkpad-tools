#!/usr/bin/env python

# This is the binary to be placed in /usr/local/bin

import Handlers

print(Handlers.Battery().getBatteryHealth())
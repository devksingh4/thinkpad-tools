#!/usr/bin/env python3

# This is the binary to be placed in /usr/local/bin

import os
import sys

import Handlers
import configparser

euid = os.geteuid()
if euid != 0:
    print("thinkpad-tools.py not started as root. Requesting root access...")
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    # the next line replaces the currently-running process with the sudo
    os.execlpe('sudo', *args)


bat1health, bat2health = Handlers.Battery().getBatteryHealth()
tp_sens, tp_speed = Handlers.Trackpoint().getValues()
bat1start, bat1stop, bat2start, bat2stop = Handlers.Battery().getBatteryThreshold()
print("-----Battery---- \n")
print("-----Battery Health-----")
print("The health of battery one (internal battery) is " + str(bat1health) + "%.")
print("The health of battery two (removeable battery) is " + str(bat2health) + "%. \n")
print("-----Charge Thresholds-----")
if bat1start != False:
    print("Battery 1 starts charging at " + bat1start + "%")
    print("Battery 1 stops charging at " + bat1stop + "% \n") 
if bat2start != False:   
    print("Battery 2 starts charging at " + bat2start + "%")
    print("Battery 2 starts charging at " + bat2stop + "% \n")

print("-----Trackpoint-----")
print("Trackpoint sensitivity is set to " + str(tp_sens.strip("\n")) + " out of 255.")
print("Trackpoint speed is set to " + str(tp_speed.strip("\n")) + " out of 255. \n")

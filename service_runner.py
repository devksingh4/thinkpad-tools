import os
import sys

import Handlers
import configparser

config = configparser.ConfigParser()
config.read('/etc/thinkpad_tools/config.ini')

trackpoint_sensitivity = config['TRACKPOINT']['SENSITIVITY']
trackpoint_speed = config['TRACKPOINT']['SPEED']

bat1_start_threshold = config['BATTERY']['BAT1_START_THRESHOLD']
bat1_stop_threshold = config['BATTERY']['BAT1_STOP_THRESHOLD']

bat2_start_threshold = config['BATTERY']['BAT2_START_THRESHOLD']
bat2_stop_threshold = config['BATTERY']['BAT2_STOP_THRESHOLD']

euid = os.geteuid()
if euid != 0:
    print("service_runner.pys not started as root. Requesting root access...")
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    # the next line replaces the currently-running process with the sudo
    os.execlpe('sudo', *args)


Handlers.Trackpoint(trackpoint_sensitivity, trackpoint_speed).setValues()
Handlers.Battery(bat1_start_threshold, bat2_start_threshold, bat1_stop_threshold, bat2_stop_threshold).setBatteryThreshold()
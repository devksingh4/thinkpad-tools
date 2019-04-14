import os
import sys

from Handlers import TrackpointConfig
import configparser

config = configparser.ConfigParser()
config.read('/etc/thinkpad_tools/config.ini')

trackpoint_sensitivity = config['TRACKPOINT']['SENSITIVITY']
trackpoint_speed = config['TRACKPOINT']['SPEED']

euid = os.geteuid()
if euid != 0:
    print("service_runner.pys not started as root. Requesting root access...")
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    # the next line replaces the currently-running process with the sudo
    os.execlpe('sudo', *args)


TrackpointConfig(trackpoint_sensitivity, trackpoint_speed).setValues()

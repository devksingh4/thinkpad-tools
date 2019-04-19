# cmd.py

import logging
import pathlib
import argparse

from .battery import BatteryHandler
from .trackpoint import TrackPointHandler

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = pathlib.Path('/etc/thinkpad-tool/')
DEFAULT_CONFIG_PATH = BASE_DIR / 'config.ini'

USAGE_HEAD = '''\
thinkpad-tool <property> <action> [<args>]

Supported properties are:
    trackpoint      Things related to TrackPoints
    battery         Things related to batteries
    
'''

USAGE_EXAMPLES = '''\
Examples:

thinkpad-tool trackpoint status
thinkpad-tool trackpoint set-sensitivity 20
'''


def commandline_parser(unparsed_args: None or list = None):
    ap = argparse.ArgumentParser(
        prog='thinkpad-tool',
        description='Tool for ThinkPads',
        usage=USAGE_HEAD,
        epilog=USAGE_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument('property', type=str, help='Property going to take action')
    prop = str(ap.parse_args(unparsed_args[0:1]).property).lower()
    if prop == 'trackpoint':
        parser = TrackPointHandler()
        parser.run(unparsed_args[1:])
    if prop == 'battery':
        parser = BatteryHandler()
        parser.run(unparsed_args[1:])

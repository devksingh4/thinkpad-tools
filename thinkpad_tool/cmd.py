# cmd.py

"""
Commandline parser
"""


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
thinkpad-tool battery list
thinkpad-tool battery status all
'''


def commandline_parser(unparsed_args: None or list = None):
    """
    Parse the first argument and call the right handler
    :param unparsed_args: Unparsed arguments
    :return: Nothing
    """
    parser = argparse.ArgumentParser(
        prog='thinkpad_tool',
        description='Tool for ThinkPads',
        usage=USAGE_HEAD,
        epilog=USAGE_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('property', type=str, help='Property going to take action')
    prop = str(parser.parse_args(unparsed_args[0:1]).property).lower()
    if prop == 'trackpoint':
        handler = TrackPointHandler()
        handler.run(unparsed_args[1:])
    if prop == 'battery':
        handler = BatteryHandler()
        handler.run(unparsed_args[1:])

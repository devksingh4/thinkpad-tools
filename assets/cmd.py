# cmd.py

"""
Commandline parser
"""


import logging
import pathlib
import argparse

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = pathlib.Path('/etc/thinkpad-tool/')
DEFAULT_CONFIG_PATH = BASE_DIR / 'config.ini'

USAGE_HEAD = '''\
thinkpad-tools <property> <action> [<args>]

Supported properties are:
    trackpoint      Things related to TrackPoints
    battery         Things related to batteries
    undervolt       Things related to undervolting
    persistence     Things related to editing persistence
'''

USAGE_EXAMPLES = '''\
Examples:

thinkpad-tools trackpoint status
thinkpad-tools trackpoint set-sensitivity 20
thinkpad-tools battery list
thinkpad-tools battery status all
thinkpad-tools undervolt set-core -20
thinkpad-tools undervolt status
thinkpad-tools persistence edit
'''


def commandline_parser(unparsed_args: None or list = None):
    """
    Parse the first argument and call the right handler
    :param unparsed_args: Unparsed arguments
    :return: Nothing
    """
    parser = argparse.ArgumentParser(
        prog='thinkpad-tools',
        description='Tool for ThinkPads',
        usage=USAGE_HEAD,
        epilog=USAGE_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'property', type=str, help='Property going to take action')
    prop = str(parser.parse_args(unparsed_args[0:1]).property).lower()
    if prop == 'trackpoint':
        from .trackpoint import TrackPointHandler
        handler = TrackPointHandler()
        handler.run(unparsed_args[1:])
    if prop == 'battery':
        from .battery import BatteryHandler
        handler = BatteryHandler()
        handler.run(unparsed_args[1:])
    if prop == 'undervolt':
        from .undervolt import UndervoltHandler
        handler = UndervoltHandler()
        handler.run(unparsed_args[1:])
    if prop == 'persistence':
        from .persistence import PersistenceHandler
        handler = PersistenceHandler()
        handler.run(unparsed_args[1:])

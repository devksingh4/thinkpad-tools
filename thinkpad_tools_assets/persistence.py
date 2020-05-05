# persistence.py

"""
Wrapper to edit the persistent settings
"""

import os
import sys
import pathlib
import argparse
import configparser
import thinkpad_tools_assets.classes
from thinkpad_tools_assets.cmd import commandline_parser
from thinkpad_tools_assets.utils import NotSudo

try:
    if os.getuid() != 0:
        raise NotSudo("Script must be run as superuser/sudo")
except NotSudo:
    print("ERROR: This script must be run as superuser/sudo")
    sys.exit(1)

USAGE_HEAD: str = '''\
thinkpad-tools persistence <verb>

Supported verbs are:
    edit    Edit the persistent settings
    enable  Enable persistent settings
    disable Disable persistent settings
    apply   Apply the persistent settings
'''

USAGE_EXAMPLES: str = '''\
Examples:

thinkpad-tools persistence edit
thinkpad-tools persistence disable
thinkpad-tools persistence enable
thinkpad-tools persistence apply
'''


class PersistenceHandler(object):
    """
    Handler for Undervolt related commands
    """
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='thinkpad-tools persistence',
            description='Edit persistence settings',
            usage=USAGE_HEAD,
            epilog=USAGE_EXAMPLES,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument('verb', type=str, help='The action going to \
            take')

    def run(self, unparsed_args: list):
        """
        Parse and execute the command
        :param unparsed_args: Unparsed arguments for this property
        :return: Nothing
        """
        def invalid_property(prop_name: str, exit_code: int):
            """
            Print error message and exit with exit code 1
            :param prop_name: Name of the property
            :param exit_code: Exit code
            :return: Nothing, the problem exits with the given exit code
            """
            print(
                'Invalid command "%s", available properties: ' % prop_name +
                ', '.join(self.inner.__dict__.keys()),
                file=sys.stderr
            )
            exit(exit_code)

        # Parse arguments
        args: argparse.Namespace = self.parser.parse_args(unparsed_args)
        verb: str = str(args.verb).lower()

        # Commands
        if verb == 'edit':
            try:
                editor: str = os.environ['EDITOR']
            except KeyError:
                editor: str = "/usr/bin/nano"
            os.system('sudo {editor} /etc/thinkpad-tools.ini'
                      .format(editor=editor))
            return
        if verb == "enable":
            os.system('systemctl daemon-reload')
            os.system('systemctl enable thinkpad-tools.service')
            print("""To set persistent settings, please edit the file
                     '/etc/thinkpad-tools.ini'""")
            print("Persistence enabled")
            return
        if verb == "disable":
            os.system('systemctl daemon-reload')
            os.system('systemctl disable thinkpad-tools.service')
            print("Persistence disabled")
            return
        if verb == "apply":
            config: configparser.ConfigParser = configparser.ConfigParser()
            config.read('/etc/thinkpad-tools.ini')
            for section in config.sections():
                for (command, val) in config.items(section):
                    commandline_parser([section, "set-"+command, val])
            return

        # No match found
        print('Command "%s" not found' % verb, file=sys.stderr)
        exit(1)

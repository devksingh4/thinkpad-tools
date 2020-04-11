# undervolt.py

"""
Wrapper to edit the persistent settings
"""

import os
import sys
import pathlib
import argparse
import assets.classes
from assets.utils import NotSudo


if os.getuid() != 0:
    raise NotSudo("Script must be run as superuser/sudo")

USAGE_HEAD: str = '''\
thinkpad-tools persistence <verb>

Supported verbs are:
    edit  Edit the persistent settings
'''

USAGE_EXAMPLES: str = '''\
Examples:

thinkpad-tools persistence edit
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
            os.system('sudo {editor} /etc/thinkpad-tools-persistence.sh'
                      .format(editor=editor))
            return
        if verb == "enable":
            os.system('systemctl daemon-reload')
            os.system('systemctl enable thinkpad-tools.service')
            print("""To set persistent settings, please edit the file
                     '/etc/thinkpad-tools-persistence.sh'""")
            print("Persistence enabled")
            return
        if verb == "disable":
            os.system('systemctl daemon-reload')
            os.system('systemctl disable thinkpad-tools.service')
            print("Persistence disabled")
            return

        # No match found
        print('Command "%s" not found' % verb, file=sys.stderr)
        exit(1)

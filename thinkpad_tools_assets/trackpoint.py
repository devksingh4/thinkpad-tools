# trackpoint.py

"""
Trackpoint related stuff
"""

from thinkpad_tools_assets.utils import ApplyValueFailedException, NotSudo
import os
import sys
import pathlib
import argparse

try:
    if os.getuid() != 0:
        raise NotSudo("Script must be run as superuser/sudo")
except NotSudo:
    print("ERROR: This script must be run as superuser/sudo")
    sys.exit(1)

if os.path.exists("/sys/devices/rmi4-00/rmi4-00.fn03/serio2"):
    BASE_PATH = pathlib.PurePath('/sys/devices/rmi4-00/rmi4-00.fn03/serio2')
elif os.path.exists("/sys/devices/rmi4-00/rmi4-00.fn03/serio3"):
    BASE_PATH = pathlib.PurePath('/sys/devices/rmi4-00/rmi4-00.fn03/serio3')
else:
    BASE_PATH = pathlib.PurePath('/sys/devices/platform/i8042/serio1/serio2')

STATUS_TEXT = '''\
Current status:
  Sensitivity:             {sensitivity}
  Speed:                   {speed}\
'''

USAGE_HEAD: str = '''\
thinkpad-tools trackpoint <verb> [argument]

Supported verbs are:
    status              Print all properties
    set-<property>      Set value
    get-<property>      Get property
    disable             Disable trackpoint
Available properties: sensitivity, speed
'''

USAGE_EXAMPLES: str = '''\
Examples:

thinkpad-tools trackpoint status
thinkpad-tools trackpoint set-sensitivity 20
thinkpad-tools trackpoint get-speed
thinkpad-tools trackpoint disable
'''


class TrackPoint(object):
    """
    Class to handle requests related to TrackPoints
    """

    def __init__(
            self,
            sensitivity: int or None = None,
            speed: int or None = None
    ):
        self.sensitivity = sensitivity
        self.speed = speed

    def read_values(self):
        """
        Read values from the system
        :return: Nothing
        """
        for prop in self.__dict__.keys():
            file_path: str = str(BASE_PATH / prop)
            if os.path.isfile(file_path):
                with open(file_path) as file:
                    self.__dict__[prop] = file.readline()
            else:
                self.__dict__[prop] = None

    def set_values(self):
        """
        Set values to the system
        :return: Nothing
        """
        success: bool = True
        failures: list = list()
        for prop in self.__dict__.keys():
            file_path: str = str(BASE_PATH / prop)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'w') as file:
                        file.write(self.__dict__[prop])
                except Exception as e:
                    success = False
                    failures.append(str(e))
        if not success:
            raise ApplyValueFailedException(', '.join(failures))

    def disableTrackpoint(self):
        """
        Disable the trackpoint
        :return: Nothing
        """
        success: bool = True
        failures: list = list()
        for prop in self.__dict__.keys():
            file_path: str = str(BASE_PATH / prop)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'w') as file:
                        file.write('0')
                except Exception as e:
                    success = False
                    failures.append(str(e))
        if not success:
            raise ApplyValueFailedException(', '.join(failures))

    def get_status_str(self) -> str:
        """
        Return status string
        :return: str: status string
        """
        return STATUS_TEXT.format(
            sensitivity=self.sensitivity or 'Unknown',
            speed=self.speed or 'Unknown'
        )


class TrackPointHandler(object):
    """
    Handler for TrackPoint related commands
    """

    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='thinkpad-tools trackpoint',
            description='TrackPoint related commands',
            usage=USAGE_HEAD,
            epilog=USAGE_EXAMPLES,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument(
            'verb', type=str, help='The action going to take')
        self.parser.add_argument(
            'arguments', nargs='*', help='Arguments of the action')
        self.inner: TrackPoint = TrackPoint()

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

        # Read values from the system
        self.inner.read_values()

        # Commands
        if verb == 'status':
            print(self.inner.get_status_str())
            return

        if verb.startswith('set-'):
            try:
                prop: str = verb.split('-', maxsplit=1)[1]
            except IndexError:
                invalid_property(verb, 1)
                return
            if prop not in self.inner.__dict__.keys():
                invalid_property(prop, 1)
            self.inner.__dict__[prop] = str(''.join(args.arguments))
            self.inner.set_values()
            print(self.inner.get_status_str())
            return

        if verb.startswith('get-'):
            try:
                prop: str = verb.split('-', maxsplit=1)[1]
            except IndexError:
                invalid_property(verb, 1)
                return
            if not hasattr(self.inner, prop):
                invalid_property(prop, 1)
            if not self.inner.__dict__[prop]:
                print('Unable to read %s' % prop)
                exit(1)
            print(self.inner.__dict__[prop])
            return
        if verb == 'disable':
            self.inner.disableTrackpoint()
            print(self.inner.get_status_str())
            return
        # No match found
        print('Command "%s" not found' % verb, file=sys.stderr)
        exit(1)

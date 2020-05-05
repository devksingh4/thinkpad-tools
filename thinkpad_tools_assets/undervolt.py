# undervolt.py

"""
Undervolt related stuff
"""

import os
import sys
import pathlib
import argparse
import thinkpad_tools_assets.classes
from thinkpad_tools_assets.utils import ApplyValueFailedException, NotSudo


try:
    if os.getuid() != 0:
        raise NotSudo("Script must be run as superuser/sudo")
except NotSudo:
    print("ERROR: This script must be run as superuser/sudo")
    sys.exit(1)

# PLANE KEY:
# Plane 0: Core
# Plane 1: GPU
# Plane 2: Cache
# Plane 3: Uncore
# Plane 4: Analogio

STATUS_TEXT = '''\
Current status:
  Core:                    {core}\n
  GPU:                     {gpu}\n
  Cache:                   {cache}\n
  Uncore:                  {uncore}\n
  Analogio:                {analogio}\n
'''
USAGE_HEAD: str = '''\
thinkpad-tools undervolt <verb> [argument]

Supported verbs are:
    status          Print all properties
    set-<property>  Set value
    get-<property>  Get property
Available properties: core, gpu, cache, uncore, analogio
'''

USAGE_EXAMPLES: str = '''\
Examples:

thinkpad-tools trackpoint status
thinkpad-tools trackpoint set-core -20
thinkpad-tools trackpoint get-gpu
'''


class Undervolt(object):
    """
    Class to handle requests related to Undervolting
    """

    def __init__(
            self,
            core: float or None = None,
            gpu: float or None = None,
            cache: float or None = None,
            uncore: float or None = None,
            analogio: float or None = None,
    ):
        # self.__register: str = "0x150"
        # self.__undervolt_value: str = "0x80000"
        self.core = core
        self.gpu = gpu
        self.cache = cache
        self.uncore = uncore
        self.analogio = analogio

    def read_values(self):
        """
        Read values from the system
        :return: Nothing
        """
        success = True
        failures: list = list()
        system = thinkpad_tools_assets.classes.UndervoltSystem()
        for prop in self.__dict__.keys():
            plane: int = 0
            if prop == "core":
                pass
            if prop == "gpu":
                plane = 1
            if prop == "cache":
                plane = 2
            if prop == "uncore":
                plane = 3
            if prop == "analogio":
                plane = 4
            try:
                h: str = system.readUndervolt(plane)
            except Exception as e:
                success = False
                failures.append(str(e))
        if not success:
            raise ApplyValueFailedException(', '.join(failures))
        self.__dict__[prop] = h

    def set_values(self):
        """
        Set values to the system MSR using undervolt function
        :return: Nothing
        """
        system = thinkpad_tools_assets.classes.UndervoltSystem()
        success: bool = True
        failures: list = list()
        for prop in self.__dict__.keys():
            if self.__dict__[prop] is None:
                continue
            plane: int = 0
            if prop == "core":
                pass
            if prop == "gpu":
                plane = 1
            if prop == "cache":
                plane = 2
            if prop == "uncore":
                plane = 3
            if prop == "analogio":
                plane = 4
            try:
                system.applyUndervolt(int(self.__dict__[prop]), plane)
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
            core=self.core or 'Unknown',
            gpu=self.gpu or 'Unknown',
            cache=self.cache or 'Unknown',
            uncore=self.uncore or 'Unknown',
            analogio=self.analogio or 'Unknown'
        )


class UndervoltHandler(object):
    """
    Handler for Undervolt related commands
    """
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='thinkpad-tools undervolt',
            description='Undervolt related commands',
            usage=USAGE_HEAD,
            epilog=USAGE_EXAMPLES,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument('verb', type=str, help='The action going to \
            take')
        self.parser.add_argument(
            'arguments', nargs='*', help='Arguments of the action')
        self.inner: Undervolt = Undervolt()

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
            print(self.inner.__dict__[prop])
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

        # No match found
        print('Command "%s" not found' % verb, file=sys.stderr)
        exit(1)

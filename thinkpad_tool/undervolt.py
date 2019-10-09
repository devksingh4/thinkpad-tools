# undervolt.py

"""
Undervolt related stuff
"""

import os
import glob
import sys
import pathlib
import argparse
import struct
if os.geteuid() != 0:
    # os.execvp() replaces the running process, rather than launching a child
    # process, so there's no need to exit afterwards. The extra "sudo" in the
    # second parameter is required because Python doesn't automatically set $0
    # in the new process.
    os.execvp("sudo", ["sudo"] + sys.argv)

# PLANE KEY:
# Plane 0: Core 
# Plane 1: GPU
# Plane 2: Cache
# Plane 3: Uncore
# Plane 4: Analogio

STATUS_TEXT = '''\
Current status:
  Core:                    {core}\
  GPU:                     {gpu}\
  Cache:                   {cache}\
  Uncore:                  {uncore}\
  Analogio:                {analogio}\
'''
USAGE_HEAD: str = '''\
thinkpad-tool undervolt <verb> [argument]

Supported verbs are:
    status          Print all properties
    set-<property>  Set value
    get-<property>  Get property
    
Available properties: core, gpu, cache, uncore, analogio
'''

USAGE_EXAMPLES: str = '''\
Examples:

thinkpad-tool trackpoint status
thinkpad-tool trackpoint set-core -20
thinkpad-tool trackpoint get-gpu
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
        self.__register: str = "0x150"
        self.__undervolt_value: str = "0x80000"
        self.core = core
        self.gpu = gpu
        self.cache = cache
        self.uncore = uncore
        self.analogio = analogio
    def undervolt(self, mv, plane):
        """
        Apply undervolt to system MSR for Intel-based systems
        :return: int error: error code to pass
        """
        error: int = 0
        uv_value: str = format(0xFFE00000&( (round(mv*1.024)&0xFFF) <<21), '08x').upper()
        final_val: int = int(("0x80000" + str(plane) + "11" + uv_value), 16)
        n: list = glob.glob('/dev/cpu/[0-9]*/msr')
        for c in n:
            f: int = os.open(c, os.O_WRONLY)
            os.lseek(f, 0x150, os.SEEK_SET) # MSR register 0x150
            os.write(f, struct.pack('Q', final_val)) # Write final val
            os.close(f)
        if not n:
            raise OSError("MSR not available. Is Secure Boot Disabled? If not, it must be disabled for this to work.")
            error = 1
        return error
    def read_values(self):
        """
        Read values from the system
        :return: Nothing
        """
        for prop in self.__dict__.keys():
            pass # insert code here

    def set_values(self):
        """
        Set values to the system MSR using undervolt function
        :return: Nothing
        """
        undervolt = UndervoltHandler()
        success: bool = True
        failures: list = list()
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
            error: int = undervolt(self.__dict__[prop], plane)
            if error != 0:
                success = False
                failures.append(str(error))
        if not success:
            raise ApplyValueFailedException(', '.join(failures))

    def get_status_str(self) -> str:
        """
        Return status string
        :return: str: status string
        """
        return STATUS_TEXT.format(
            core=self.core or 'Unknown\n',
            gpu=self.gpu or 'Unknown\n',
            cache=self.cache or 'Unknown\n',
            uncore=self.uncore or 'Unknown\n',
            analogio = self.analogio or 'Unknown\n'
        )


class UndervoltHandler(object):
    """
    Handler for Undervolt related commands
    """
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='thinkpad-tool undervolt',
            description='Undervolt related commands',
            usage=USAGE_HEAD,
            epilog=USAGE_EXAMPLES,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument('verb', type=str, help='The action going to take')
        self.parser.add_argument('arguments', nargs='*', help='Arguments of the action')
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
                'Invalid command "%s", available properties: ' % prop_name +\
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

        # No match found
        print('Command "%s" not found' % verb, file=sys.stderr)
        exit(1)

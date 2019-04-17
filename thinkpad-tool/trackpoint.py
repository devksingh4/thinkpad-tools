# trackpoint.py

import os
import sys
import pathlib
import argparse

from .utils import ApplyValueFailedException

BASE_PATH = pathlib.PurePath('/sys/devices/platform/i8042/serio1/serio2')

STATUS_TEXT = '''\
Current settings:
Sensitivity - {sensitivity}
Speed       - {speed}\
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

    def get_status_str(self) -> str:
        """
        Return string
        :return:
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
            prog='thinkpad-tool trackpoint',
            description='TrackPoint related commands',
        )
        self.parser.add_argument('verb', type=str, help='The action going to take')
        self.parser.add_argument('arguments', nargs='*', help='Arguments of the action')
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
            :param prop_name:
            :return:
            """
            print(
                'Invalid property "%s", available properties: ' % prop_name +\
                ', '.join(self.inner.__dict__.keys()),
                file=sys.stderr
            )
            exit(exit_code)
        args: argparse.Namespace = self.parser.parse_args(unparsed_args)
        verb: str = str(args.verb).lower()
        self.inner.read_values()
        if verb == 'status':
            print(self.inner.get_status_str())
        if verb.startswith('set-'):
            try:
                prop: str = verb.split('-', maxsplit=1)[1]
            except IndexError:
                invalid_property(prop, 1)
            if prop not in self.inner.__dict__.keys():
                invalid_property(prop, 1)
            self.inner.__dict__[prop] = int(''.join(args.arguments))
            self.inner.set_values()
            print(self.inner.get_status_str())
        if verb.startswith('get-'):
            try:
                prop: str = verb.split('-', maxsplit=1)[1]
            except IndexError:
                invalid_property(prop, 1)
            if not hasattr(self.inner, prop):
                invalid_property(prop, 1)
            if not self.inner.__dict__[prop]:
                print('Unable to read %s' % prop)
                exit(1)
            print(self.inner.__dict__[prop])

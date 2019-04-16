# trackpoint.py

import os
import pathlib
import argparse

from .utils import ApplyValueFailedException

BASE_PATH = pathlib.PurePath('/sys/devices/platform/i8042/serio1/serio2')

STATUS_TEXT = '''\
Current settings:
Sensitivity - {sensitivity}
Speed       - {speed}
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
        for prop in self.__dict__.keys():
            file_path: str = str(BASE_PATH / prop)
            if os.path.isfile(file_path):
                with open(file_path) as file:
                    self.__dict__[prop] = file.readline()
            else:
                self.__dict__[prop] = None

    def set_values(self):
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
        args: argparse.Namespace = self.parser.parse_args(unparsed_args)
        verb: str = str(args.verb).lower()
        if verb == 'status':
            self.inner.read_values()
            print(self.inner.get_status_str())
        if verb.startswith('set-'):
            try:
                prop: str = verb.split('-', maxsplit=1)[1]
            except IndexError:
                print('Invalid property')
                return
            if prop not in self.inner.__dict__.keys():
                print('Invalid property, available properties: ' + ', '.join(self.inner.__dict__.keys()))
                return
            self.inner.__dict__[prop] = int(''.join(args.arguments))
            self.inner.set_values()
            print(self.inner.get_status_str())

"""
Battery related stuff
"""


import os
import re
import sys
import pathlib
import argparse
from thinkpad_tools_assets.utils import ApplyValueFailedException, NotSudo

BASE_DIR = pathlib.PurePath('/sys/class/power_supply/')

PROPERTIES: dict = {
    'alarm': 0,
    'capacity': 100, 'capacity_level': 'Unknown',
    'charge_start_threshold': 0, 'charge_stop_threshold': 100,
    'cycle_count': 0,
    'energy_full': 0, 'energy_full_design': 0, 'energy_now': 0,
    'manufacturer': 'Unknown', 'model_name': 'Unknown',
    'power_now': False, 'present': True,
    'serial_number': 0,
    'status': 'Unknown',
    'technology': 'Unknown', 'type': 'Unknown',
    'voltage_min_design': 0, 'voltage_now': 0
}

STRING_PROPERTIES: list = [
    'capacity_level',
    'manufacturer', 'model_name',
    'status',
    'technology', 'type'
]

BOOLEAN_PROPERTIES: list = [
    'power_now', 'present'
]

EDITABLE_PROPERTIES: list = [
    'charge_start_threshold', 'charge_stop_threshold'
]

STATUS_STR_TEMPLATE: str = '''\
Status of battery "{name}":
  Alarm:                    {alarm} Wh
  Capacity level:           {capacity_level}
  Charge start threshold:   {charge_start_threshold}%
  Charge stop threshold:    {charge_stop_threshold}%
  Cycle count:              {cycle_count}
  Current capacity:         {energy_full} Wh
  Design capacity:          {energy_full_design} Wh
  Battery health:           {battery_health}%
  Current energy:           {energy_now} Wh
  Manufacturer:             {manufacturer}
  Model name:               {model_name}
  In use:                   {power_now}
  Present:                  {present}
  Serial number:            {serial_number}
  Status:                   {status}
  Technology:               {technology}
  Type:                     {type}
  Minimum design voltage:   {voltage_min_design}
  Current voltage:          {voltage_now}\
'''

USAGE_HEAD: str = '''\
thinkpad-tools battery <verb> <battery> [argument]

Regex can be used in <battery> to match multiple batteries

Supported verbs are:
    list            List available batteries
    status          Print all properties
    set-<property>  Set value
    get-<property>  Get property
Readable properties: {properties}
Editable properties: {editable_properties}
'''.format(
    properties=', '.join(PROPERTIES.keys()),
    editable_properties=', '.join(EDITABLE_PROPERTIES)
)

USAGE_EXAMPLES: str = '''\
Examples:

thinkpad-tools battery list
thinkpad-tools battery set-charge-start-threshold all 80
thinkpad-tools battery set-stop-start-threshold BAT0 90
thinkpad-tools battery get-battery-health
'''


class Battery(object):
    """
    Class to handle requests related to Batteries
    """

    def __init__(self, name: str = 'BAT0', **kwargs):
        self.name: str = name
        self.path: pathlib.PurePath = BASE_DIR / self.name
        for prop, default_value in PROPERTIES.items():
            if prop in kwargs.keys():
                if type(kwargs[prop]) == type(default_value):
                    self.__dict__[prop] = kwargs[prop]
            self.__dict__[prop] = default_value
        self.battery_health: int = 100

    def read_values(self):
        """
        Read values from the system
        :return: Nothing
        """
        for prop in self.__dict__.keys():
            path = str(self.path / prop)
            if os.path.isfile(path):
                with open(path) as file:
                    content = file.readline()
                if prop in STRING_PROPERTIES:
                    self.__dict__[prop] = str(content).strip()
                elif prop in BOOLEAN_PROPERTIES:
                    self.__dict__[prop] = bool(content)
                else:
                    self.__dict__[prop] = int(content)
        self.battery_health: int = int(
            self.energy_full / self.energy_full_design * 100)

    def set_values(self):
        """
        Set values to the system
        :return: Nothing
        """
        success: bool = True
        failures: list = list()
        for prop in EDITABLE_PROPERTIES:
            if prop not in self.__dict__.keys():
                success = False
                failures.append(
                    'Property "%s" not found in current object' % prop)
                continue
            path = str(self.path / prop)
            if os.path.isfile(path):
                try:
                    with open(path, 'w') as file:
                        # TODO: Handle different types of properties
                        file.write(str(self.__dict__[prop]))
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
        return STATUS_STR_TEMPLATE.format(
            name=str(self.name),
            alarm=str(self.alarm / 1000000),
            capacity=str(self.capacity),
            capacity_level=str(self.capacity_level),
            charge_start_threshold=str(self.charge_start_threshold),
            charge_stop_threshold=str(self.charge_stop_threshold),
            cycle_count=str(self.cycle_count),
            energy_full=str(self.energy_full / 1000000),
            energy_full_design=str(self.energy_full_design / 1000000),
            battery_health=str(self.battery_health),
            energy_now=str(self.energy_now / 1000000),
            manufacturer=str(self.manufacturer),
            model_name=str(self.model_name),
            power_now='Yes' if self.power_now else 'No',
            present='Yes' if self.present else 'No',
            serial_number=str(self.serial_number),
            status=str(self.status),
            technology=str(self.technology),
            type=str(self.type),
            voltage_min_design=str(self.voltage_min_design),
            voltage_now=str(self.voltage_now)
        )


class BatteryHandler(object):
    """
    Handler for battery related commands
    """

    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='thinkpad-tools battery',
            description='Battery related commands',
            usage=USAGE_HEAD,
            epilog=USAGE_EXAMPLES,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument(
            'verb', type=str, help='The action going to take')
        self.parser.add_argument(
            'battery', nargs='?', type=str, help='The battery')
        self.parser.add_argument(
            'arguments', nargs='*', help='Arguments of the action')
        self.inner: dict = dict()
        for name in os.listdir(str(BASE_DIR)):
            if not name.startswith('BAT'):
                continue
            self.inner[name]: Battery = Battery(name)

    def run(self, unparsed_args: list):
        """
        Parse and execute the commands
        :param unparsed_args: Unparsed arguments
        :return: Nothing
        """
        def find_match(battery_name: str) -> list:
            """
            Find matched batteries
            :param battery_name: name(regex) of the battery
            :return: list: List of matched battery/batteries
            """
            if battery_name.lower() == 'all':
                return list(self.inner.keys())
            try:
                pattern: re.Pattern = re.compile(battery_name)
            except re.error as e:
                print(
                    'Invalid matching pattern "%s", %s' % (
                        battery_name, str(e)),
                    file=sys.stderr
                )
                exit(1)
            return list(filter(pattern.match, self.inner.keys()))

        def invalid_battery(battery_name: str):
            """
            No battery found for the given pattern
            :param battery_name: pattern of the battery
            :return: Nothing, the program exits with status code 1
            """
            print(
                'No battery found for pattern"%s", \
                available battery(ies): ' % battery_name +
                ', '.join(self.inner.keys()),
                file=sys.stderr
            )
            exit(1)

        def invalid_property(
                prop_name: str, battery_name: str, exit_code: int):
            """
            Invalid property
            :param prop_name: Name of the property
            :param battery_name: Name of the battery
            :param exit_code: Exit code going to be used
            :return: Nothing, the program exits with the given status code
            """
            print(
                'Invalid property "%s", available properties: ' % prop_name +
                ', '.join(self.inner[battery_name].__dict__.keys()),
                file=sys.stderr
            )
            exit(exit_code)

        # Parse arguments
        args: argparse.Namespace = self.parser.parse_args(unparsed_args)
        verb: str = str(args.verb).lower()
        if not args.battery:
            battery: str = 'all'
        else:
            battery: str = str(args.battery)
        names: list = find_match(battery)

        # Read values from the system
        for name in names:
            self.inner[name].read_values()

        # Commands
        if verb == 'list':
            print(' '.join(self.inner.keys()))
            return

        if verb == 'status':
            result: list = list()
            for name in names:
                result.append(self.inner[name].get_status_str())
            if len(result) == 0:
                invalid_battery(battery)
            print('\n'.join(result))
            return

        if verb.startswith('set-'):
            if os.getuid() != 0:
                raise NotSudo("Script must be run as superuser/sudo")
            try:
                prop: str = verb.split('-', maxsplit=1)[1].replace('-', '_')
            except IndexError:
                print('Invalid command', file=sys.stderr)
                exit(1)
            for name in names:
                if (prop not in EDITABLE_PROPERTIES) or\
                        (prop not in self.inner[name].__dict__.keys()):
                    invalid_property(prop, name, 1)
                value: str = ''.join(args.arguments)
                if not value:
                    print('Value is needed', file=sys.stderr)
                    exit(1)
                    return
                self.inner[name].__dict__[prop] = int(value)
                try:
                    self.inner[name].set_values()
                except ApplyValueFailedException as e:
                    print(str(e), file=sys.stderr)
                    exit(1)
                print(value)
            return

        if verb.startswith('get-'):
            try:
                prop: str = verb.split('-', maxsplit=1)[1].replace('-', '_')
            except IndexError:
                print('Invalid command', file=sys.stderr)
                exit(1)
            result: list = list()
            for name in names:
                if prop not in self.inner[name].__dict__.keys():
                    invalid_property(prop, name, 1)
                result.append(str(self.inner[name].__dict__[prop]))
            print(' '.join(result))
            return

        # No match found
        print('Command "%s" not found' % verb, file=sys.stderr)
        exit(1)

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
class TrackPoint(object):
    """
    Class to handle requests related to TrackPoints
    """

    def __init__(
            self,
            core: float or None = None,
            gpu: float or None = None,
            cache: float or None = None,
            uncore: float or None = None,
            analogio: float or None = None,
    ):
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
        for prop in self.__dict__.keys():
            pass # insert code here

    def set_values(self):
        """
        Set values to the system MSR using UndervoltHandler class
        :return: Nothing
        """
        undervolt = UndervoltHandler()
        success: bool = True
        failures: list = list()
        for prop in self.__dict__.keys():
            file_path: str = str(BASE_PATH / prop)
            if os.path.isfile(file_path):
                try:
                    pass # insert code here
                except Exception as e:
                    pass # insert code here
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
            analogio = self.analogio or 'Unknown'
        )


class UndervoltHandler(object):
    """
    Handler for Undervolt related commands
    """
    def __init__(self):
        self.__register: str = "0x150"
        self.__undervolt_value: str = "0x80000"

    def undervolt(self, mv, plane):
        """
        Apply undervolt to system MSR for Intel-based systems
        :return: Nothing
        """
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

# hi = UndervoltHandler()
# hi.undervolt(-20,2)
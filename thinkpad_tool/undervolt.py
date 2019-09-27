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

# STATUS_TEXT = '''\
# Current status:
#   Sensitivity:             {sensitivity}
#   Speed:                   {speed}\
# '''

# USAGE_HEAD: str = '''\
# thinkpad-tool undervolt <verb> [argument]

# Supported verbs are:
#     status          Print all properties
#     set-<property>  Set value
#     get-<property>  Get property
    
# Available properties: sensitivity, speed
# '''

# USAGE_EXAMPLES: str = '''\
# Examples:

# thinkpad-tool trackpoint status
# thinkpad-tool trackpoint set-sensitivity 20
# thinkpad-tool trackpoint get-speed
# '''

# planned undervolts: core, cache, analogio, uncore, gpu

class UndervoltHandler(object):
    def __init__(self):
        self.__register = "0x150"
        self.__undervolt_value = "0x80000"

    def undervolt(self, mv, plane):
            uv_value = format(0xFFE00000&( (round(mv*1.024)&0xFFF) <<21), '08x').upper()
            final_val = int(("0x80000" + str(plane) + "11" + uv_value), 16)
            n = glob.glob('/dev/cpu/[0-9]*/msr')
            for c in n:
                f = os.open(c, os.O_WRONLY)
                os.lseek(f, 0x150, os.SEEK_SET) # MSR register 0x150
                os.write(f, struct.pack('Q', final_val)) # Write final val
                os.close(f)
            if not n:
                raise OSError("MSR not available")

hi = UndervoltHandler()
hi.undervolt(-90, 0)
hi.undervolt(-90, 2)

# plane 0 core, plane 1 gpu plane 21cache plane 3 uncore plane 4 analogio
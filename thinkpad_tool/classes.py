import os
import glob
import sys
import struct
from struct import pack, unpack


class UndervoltSystem(object):
    def __init__(self):
        pass

    def applyUndervolt(self, mv, plane):
        """
        Apply undervolt to system MSR for Intel-based systems
        :return: int error: error code to pass
        """
        error = 0
        uv_value = format(
            0xFFE00000 & ((round(mv*1.024) & 0xFFF) << 21), '08x').upper()
        final_val = int(("0x80000" + str(plane) + "11" + uv_value), 16)
        n: list = glob.glob('/dev/cpu/[0-9]*/msr')
        for c in n:
            f: int = os.open(c, os.O_WRONLY)
            os.lseek(f, 0x150, os.SEEK_SET)  # MSR register 0x150
            os.write(f, struct.pack('Q', final_val))  # Write final val
            os.close(f)
        if not n:
            raise OSError("MSR not available. Is Secure Boot Disabled? \
                If not, it must be disabled for this to work.")
            error = 1
        return error

    def readUndervolt(self, plane):
        """
        Read undervolt offset on given plane
        :return: str val: offset on plane in hex
        """
        offset: int = 0 or None
        n: str = '/dev/cpu/%d/msr' % (0,)
        f = os.open(n, os.O_RDONLY)
        os.lseek(f, 0x150, os.SEEK_SET)
        val, = unpack('Q', os.read(f, 8))  # val now contains the MSR value
        os.close(f)
        return str(val)

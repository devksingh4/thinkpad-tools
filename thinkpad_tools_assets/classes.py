import os
import glob
import sys
import struct
import subprocess
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
        return error

    def parseReadUndervolt(self, offset):
        plane = int(offset / (1 << 40))
        unpack_val_unround = offset ^ (plane << 40)
        temp = unpack_val_unround >> 21
        unpack_val = temp if temp <= 1024 else - (2048-temp)
        unpack_val_round = unpack_val / 1.024
        return f"{str(round(unpack_val_round))}"

    def readUndervolt(self, plane):
        """
        Read undervolt offset on given plane
        :return: str val: offset on plane in hex
        """
        # write read to register for cpu0
        final_val = ((1 << 63) | (plane << 40) | (1 << 36) | 0)
        f: int = os.open('/dev/cpu/0/msr', os.O_WRONLY)
        os.lseek(f, 0x150, os.SEEK_SET)  # MSR register 0x150
        os.write(f, struct.pack('Q', final_val))  # Write final val
        os.close(f)
        # now read offset
        f: int = os.open('/dev/cpu/0/msr', os.O_RDONLY)
        os.lseek(f, 0x150, os.SEEK_SET)
        offset, *_ = unpack('Q', os.read(f, 8))
        return self.parseReadUndervolt(offset)

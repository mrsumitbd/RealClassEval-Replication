from s_tui.helper_functions import cat
from sys import byteorder
from multiprocessing import cpu_count
import re

class AMDRaplMsrReader:

    def __init__(self):
        self.core_msr_files = {}
        self.package_msr_files = {}
        for i in range(cpu_count()):
            curr_core_id = int(cat('/sys/devices/system/cpu/cpu' + str(i) + '/topology/core_id', binary=False))
            if curr_core_id not in self.core_msr_files:
                self.core_msr_files[curr_core_id] = '/dev/cpu/' + str(i) + '/msr'
            curr_package_id = int(cat('/sys/devices/system/cpu/cpu' + str(i) + '/topology/physical_package_id', binary=False))
            if curr_package_id not in self.package_msr_files:
                self.package_msr_files[curr_package_id] = '/dev/cpu/' + str(i) + '/msr'

    @staticmethod
    def read_msr(filename, register):
        f = open(filename, 'rb')
        f.seek(register)
        res = int.from_bytes(f.read(8), byteorder)
        f.close()
        return res

    def read_power(self):
        ret = []
        for i, filename in self.package_msr_files.items():
            unit_msr = self.read_msr(filename, UNIT_MSR)
            energy_factor = 0.5 ** ((unit_msr & ENERGY_UNIT_MASK) >> 8)
            package_msr = self.read_msr(filename, PACKAGE_MSR)
            ret.append(RaplStats('Package ' + str(i + 1), package_msr * energy_factor * MICRO_JOULE_IN_JOULE, 0.0))
        for i, filename in self.core_msr_files.items():
            unit_msr = self.read_msr(filename, UNIT_MSR)
            energy_factor = 0.5 ** ((unit_msr & ENERGY_UNIT_MASK) >> 8)
            core_msr = self.read_msr(filename, CORE_MSR)
            ret.append(RaplStats('Core ' + str(i + 1), core_msr * energy_factor * MICRO_JOULE_IN_JOULE, 0.0))
        return ret

    @staticmethod
    def available():
        try:
            cpuinfo = cat('/proc/cpuinfo', binary=False)
            m = re.search('vendor_id[\\s]+: ([A-Za-z]+)', cpuinfo)
            if not m or m is None:
                return False
            if m.group(1) != 'AuthenticAMD':
                return False
            m = re.search('cpu family[\\s]+: ([0-9]+)', cpuinfo)
            if int(m[1]) != 23:
                return False
        except (FileNotFoundError, PermissionError):
            return False
        try:
            open('/dev/cpu/0/msr')
            return True
        except (FileNotFoundError, PermissionError):
            return False
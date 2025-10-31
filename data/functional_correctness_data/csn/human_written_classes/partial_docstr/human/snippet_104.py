import glob
import os
import logging
from s_tui.helper_functions import cat

class RaplReader:

    def __init__(self):
        basenames = glob.glob('/sys/class/powercap/intel-rapl:*/')
        self.basenames = sorted(set({x for x in basenames}))

    def read_power(self):
        """Read power stats and return dictionary"""
        pjoin = os.path.join
        ret = list()
        for path in self.basenames:
            name = None
            try:
                name = cat(pjoin(path, 'name'), fallback=None, binary=False)
            except (IOError, OSError, ValueError) as err:
                logging.warning('ignoring %r for file %r', (err, path), RuntimeWarning)
                continue
            if name:
                try:
                    current = cat(pjoin(path, 'energy_uj'))
                    max_reading = 0.0
                    ret.append(RaplStats(name, float(current), max_reading))
                except (IOError, OSError, ValueError) as err:
                    logging.warning('ignoring %r for file %r', (err, path), RuntimeWarning)
        return ret

    @staticmethod
    def available():
        return os.path.exists('/sys/class/powercap/intel-rapl')
from os.path import join, normpath, splitext, isfile, dirname, basename
import glob

class ProGenMcus:

    def __init__(self):
        mcu_files = glob.glob(join(dirname(__file__), 'mcu', '*', '*.yaml'))
        self.mcus = {}
        for m in mcu_files:
            self.mcus[splitext(basename(m))[0]] = m

    def get_mcus(self):
        return list(self.mcus.keys())

    def get_mcu_record(self, mcu):
        if mcu in self.get_mcus():
            mcu_path = self.mcus[mcu]
            return _load_record(mcu_path)
        else:
            return None
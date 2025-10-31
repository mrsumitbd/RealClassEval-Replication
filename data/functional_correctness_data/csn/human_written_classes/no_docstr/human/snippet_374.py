from pyperf._utils import MS_WINDOWS, MAC_OS, percentile, median_abs_dev

class MemoryUsage:

    def __init__(self):
        self.mem_thread = None
        self.get_peak_profile_usage = None

    def start(self):
        if MS_WINDOWS:
            from pyperf._win_memory import get_peak_pagefile_usage
            self.get_peak_profile_usage = get_peak_pagefile_usage
        elif MAC_OS:
            from pyperf._psutil_memory import PeakMemoryUsageThread
            self.mem_thread = PeakMemoryUsageThread()
            self.mem_thread.start()
        else:
            from pyperf._linux_memory import PeakMemoryUsageThread
            self.mem_thread = PeakMemoryUsageThread()
            self.mem_thread.start()

    def get_memory_peak(self):
        if MS_WINDOWS:
            mem_peak = self.get_peak_profile_usage()
        else:
            self.mem_thread.stop()
            mem_peak = self.mem_thread.peak_usage
        if not mem_peak:
            raise RuntimeError('failed to get the memory peak usage')
        return mem_peak
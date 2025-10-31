from bcbio import utils
import toolz as tz
import math
import numpy as np
import pybedtools

class MemoizedSizes:
    """Delay calculating sizes unless needed; cache to calculate a single time.
    """

    def __init__(self, cnv_file, items):
        self.result = None
        self.cnv_file = cnv_file
        self.items = items

    def get_target_antitarget_bin_sizes(self):
        if self.result:
            return self.result
        else:
            self.result = self._calc_sizes(self.cnv_file, self.items)
            return self.result

    def _calc_sizes(self, cnv_file, items):
        """Retrieve target and antitarget bin sizes based on depth.

        Similar to CNVkit's do_autobin but tries to have a standard set of
        ranges (50bp intervals for target and 10kb intervals for antitarget).
        """
        bp_per_bin = 100000
        range_map = {'target': (100, 250), 'antitarget': (10000, 1000000)}
        target_bps = []
        anti_bps = []
        checked_beds = set([])
        for data in items:
            region_bed = tz.get_in(['depth', 'variant_regions', 'regions'], data)
            if region_bed and region_bed not in checked_beds:
                with utils.open_gzipsafe(region_bed) as in_handle:
                    for r in pybedtools.BedTool(in_handle).intersect(cnv_file):
                        if r.stop - r.start > range_map['target'][0]:
                            target_bps.append(float(r.name))
                with utils.open_gzipsafe(region_bed) as in_handle:
                    for r in pybedtools.BedTool(in_handle).intersect(cnv_file, v=True):
                        if r.stop - r.start > range_map['target'][1]:
                            anti_bps.append(float(r.name))
                checked_beds.add(region_bed)

        def scale_in_boundary(raw, round_interval, range_targets):
            min_val, max_val = range_targets
            out = int(math.ceil(raw / float(round_interval)) * round_interval)
            if out > max_val:
                return max_val
            elif out < min_val:
                return min_val
            else:
                return out
        if target_bps and np.median(target_bps) > 0:
            raw_target_bin = bp_per_bin / float(np.median(target_bps))
            target_bin = scale_in_boundary(raw_target_bin, 50, range_map['target'])
        else:
            target_bin = range_map['target'][1]
        if anti_bps and np.median(anti_bps) > 0:
            raw_anti_bin = bp_per_bin / float(np.median(anti_bps))
            anti_bin = scale_in_boundary(raw_anti_bin, 10000, range_map['antitarget'])
        else:
            anti_bin = range_map['antitarget'][1]
        return (target_bin, anti_bin)
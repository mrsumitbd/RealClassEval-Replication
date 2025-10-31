from typing import Dict, List, Optional, Tuple
import math


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.reset()

    def reset(self) -> None:
        '''Reset all metrics.'''
        # Aggregation counters
        self._runs = 0
        self._total_sequences = 0
        self._total_sequence_length = 0
        self._total_packed_length = 0
        self._total_bins = 0
        self._total_capacity = 0
        self._total_waste_space = 0
        self._total_overflow_space = 0

        # Sums for averaging per-run stats
        self._sum_overall_utilization = 0.0  # per-run effective overall utilization
        self._sum_avg_bin_utilization = 0.0
        self._sum_bin_imbalance = 0.0
        self._sum_std_bin_utilization = 0.0

        # Time metrics
        self._time_total = 0.0
        self._time_min: Optional[float] = None
        self._time_max: Optional[float] = None
        self._time_runs = 0

        # Last stats
        self._last_stats: Dict[str, float] = {}

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        '''Update metrics with a new packing solution.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
            packing_time: Optional time taken to compute the packing solution
        Returns:
            Dictionary of metrics for this packing solution
        '''
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)

        # Update aggregated counters
        self._runs += 1
        self._total_sequences += int(stats['num_sequences'])
        self._total_sequence_length += int(stats['total_sequence_length'])
        self._total_packed_length += int(stats['packed_sequence_length'])
        self._total_bins += int(stats['num_bins'])
        self._total_capacity += int(stats['total_capacity'])
        self._total_waste_space += int(stats['total_waste_space'])
        self._total_overflow_space += int(stats['total_overflow_space'])

        # Update sums for average per-run stats
        self._sum_overall_utilization += float(stats['overall_utilization'])
        self._sum_avg_bin_utilization += float(stats['avg_bin_utilization'])
        self._sum_bin_imbalance += float(stats['bin_imbalance'])
        self._sum_std_bin_utilization += float(stats['std_bin_utilization'])

        # Time metrics
        if packing_time is not None:
            self._time_total += float(packing_time)
            self._time_runs += 1
            if self._time_min is None or packing_time < self._time_min:
                self._time_min = float(packing_time)
            if self._time_max is None or packing_time > self._time_max:
                self._time_max = float(packing_time)
            stats['packing_time'] = float(packing_time)

        self._last_stats = stats
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        '''Calculate metrics for a packing solution without updating the tracker.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
        Returns:
            Dictionary of metrics for this packing solution
        '''
        num_sequences = len(sequence_lengths)
        total_sequence_length = int(sum(int(x) for x in sequence_lengths))
        num_bins = len(bins)
        capacity = int(bin_capacity)
        total_capacity = int(num_bins * capacity)

        # Compute per-bin usage, free space, overflow
        bin_usages: List[int] = []
        bin_utils: List[float] = []
        free_spaces: List[int] = []
        overflows: List[int] = []

        for b in bins:
            used = int(sum(int(sequence_lengths[i]) for i in b)) if b else 0
            bin_usages.append(used)
            util = (used / capacity) if capacity > 0 else 0.0
            bin_utils.append(util)
            free = capacity - used
            free_spaces.append(max(0, free))
            overflows.append(max(0, -free))

        # may differ from total_sequence_length if bins don't cover all seqs
        packed_sequence_length = int(sum(bin_usages))
        packing_coverage = (packed_sequence_length /
                            total_sequence_length) if total_sequence_length > 0 else 0.0

        # Overall utilization (effective, capped at 1.0) and raw (may exceed 1.0 if overflow)
        if total_capacity > 0:
            raw_overall_utilization = packed_sequence_length / total_capacity
            overall_utilization = min(
                packed_sequence_length, total_capacity) / total_capacity
        else:
            raw_overall_utilization = 0.0
            overall_utilization = 0.0

        total_waste_space = int(sum(free_spaces))
        total_overflow_space = int(sum(overflows))
        waste_ratio = (total_waste_space /
                       total_capacity) if total_capacity > 0 else 0.0
        overflow_ratio = (total_overflow_space /
                          total_capacity) if total_capacity > 0 else 0.0
        avg_waste_per_bin = (total_waste_space /
                             num_bins) if num_bins > 0 else 0.0

        # Utilization stats across bins
        if num_bins > 0:
            avg_bin_utilization = sum(bin_utils) / num_bins
            min_bin_utilization = min(bin_utils) if bin_utils else 0.0
            max_bin_utilization = max(bin_utils) if bin_utils else 0.0
            std_bin_utilization = self._std(bin_utils)
            bin_imbalance = max_bin_utilization - min_bin_utilization
            empty_bins = sum(1 for u in bin_usages if u == 0)
            overflow_bins = sum(1 for o in overflows if o > 0)
        else:
            avg_bin_utilization = 0.0
            min_bin_utilization = 0.0
            max_bin_utilization = 0.0
            std_bin_utilization = 0.0
            bin_imbalance = 0.0
            empty_bins = 0
            overflow_bins = 0

        return {
            'num_sequences': float(num_sequences),
            'total_sequence_length': float(total_sequence_length),
            'packed_sequence_length': float(packed_sequence_length),
            'packing_coverage': float(packing_coverage),
            'bin_capacity': float(capacity),
            'num_bins': float(num_bins),
            'total_capacity': float(total_capacity),
            'overall_utilization': float(overall_utilization),
            'raw_overall_utilization': float(raw_overall_utilization),
            'avg_bin_utilization': float(avg_bin_utilization),
            'min_bin_utilization': float(min_bin_utilization),
            'max_bin_utilization': float(max_bin_utilization),
            'std_bin_utilization': float(std_bin_utilization),
            'bin_imbalance': float(bin_imbalance),
            'total_waste_space': float(total_waste_space),
            'avg_waste_per_bin': float(avg_waste_per_bin),
            'waste_ratio': float(waste_ratio),
            'total_overflow_space': float(total_overflow_space),
            'overflow_bins': float(overflow_bins),
            'overflow_ratio': float(overflow_ratio),
            'empty_bins': float(empty_bins),
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        runs = self._runs
        total_capacity = self._total_capacity
        weighted_overall_utilization = (
            self._total_packed_length / total_capacity) if total_capacity > 0 else 0.0
        weighted_effective_utilization = (min(
            self._total_packed_length, total_capacity) / total_capacity) if total_capacity > 0 else 0.0
        weighted_waste_ratio = (
            self._total_waste_space / total_capacity) if total_capacity > 0 else 0.0
        weighted_overflow_ratio = (
            self._total_overflow_space / total_capacity) if total_capacity > 0 else 0.0

        avg_overall_utilization = (
            self._sum_overall_utilization / runs) if runs > 0 else 0.0
        avg_bin_utilization = (
            self._sum_avg_bin_utilization / runs) if runs > 0 else 0.0
        avg_bin_imbalance = (self._sum_bin_imbalance /
                             runs) if runs > 0 else 0.0
        avg_std_bin_utilization = (
            self._sum_std_bin_utilization / runs) if runs > 0 else 0.0

        avg_bins_per_run = (self._total_bins / runs) if runs > 0 else 0.0
        avg_sequences_per_run = (
            self._total_sequences / runs) if runs > 0 else 0.0

        time_avg = (self._time_total /
                    self._time_runs) if self._time_runs > 0 else 0.0

        return {
            'runs': float(runs),
            'total_sequences': float(self._total_sequences),
            'total_sequence_length': float(self._total_sequence_length),
            'total_packed_length': float(self._total_packed_length),
            'total_bins': float(self._total_bins),
            'total_capacity': float(total_capacity),
            'total_waste_space': float(self._total_waste_space),
            'total_overflow_space': float(self._total_overflow_space),
            'weighted_overall_utilization': float(weighted_overall_utilization),
            'weighted_effective_utilization': float(weighted_effective_utilization),
            'weighted_waste_ratio': float(weighted_waste_ratio),
            'weighted_overflow_ratio': float(weighted_overflow_ratio),
            'avg_bins_per_run': float(avg_bins_per_run),
            'avg_sequences_per_run': float(avg_sequences_per_run),
            'avg_overall_utilization': float(avg_overall_utilization),
            'avg_bin_utilization': float(avg_bin_utilization),
            'avg_bin_imbalance': float(avg_bin_imbalance),
            'avg_std_bin_utilization': float(avg_std_bin_utilization),
            'runs_with_time': float(self._time_runs),
            'time_total': float(self._time_total),
            'time_avg': float(time_avg),
            'time_min': float(self._time_min) if self._time_min is not None else 0.0,
            'time_max': float(self._time_max) if self._time_max is not None else 0.0,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        agg = self.get_aggregated_stats()
        print('Packing Metrics (Aggregated):')
        print(f'  Runs: {int(agg["runs"])}')
        print(f'  Total sequences: {int(agg["total_sequences"])}')
        print(f'  Total sequence length: {int(agg["total_sequence_length"])}')
        print(f'  Total packed length: {int(agg["total_packed_length"])}')
        print(f'  Total bins: {int(agg["total_bins"])}')
        print(f'  Total capacity: {int(agg["total_capacity"])}')
        print(
            f'  Weighted overall utilization: {agg["weighted_overall_utilization"]:.4f}')
        print(
            f'  Weighted effective utilization: {agg["weighted_effective_utilization"]:.4f}')
        print(f'  Weighted waste ratio: {agg["weighted_waste_ratio"]:.4f}')
        print(
            f'  Weighted overflow ratio: {agg["weighted_overflow_ratio"]:.4f}')
        print(f'  Avg bins/run: {agg["avg_bins_per_run"]:.2f}')
        print(f'  Avg sequences/run: {agg["avg_sequences_per_run"]:.2f}')
        print(
            f'  Avg overall utilization (per-run): {agg["avg_overall_utilization"]:.4f}')
        print(
            f'  Avg bin utilization (per-run): {agg["avg_bin_utilization"]:.4f}')
        print(f'  Avg bin imbalance (per-run): {agg["avg_bin_imbalance"]:.4f}')
        print(
            f'  Avg std(bin utilization) (per-run): {agg["avg_std_bin_utilization"]:.4f}')
        print(f'  Total waste space: {int(agg["total_waste_space"])}')
        print(f'  Total overflow space: {int(agg["total_overflow_space"])}')
        if int(agg['runs_with_time']) > 0:
            print('  Timing:')
            print(f'    Runs with time: {int(agg["runs_with_time"])}')
            print(
                f'    Total: {agg["time_total"]:.6f}s  Avg: {agg["time_avg"]:.6f}s  Min: {agg["time_min"]:.6f}s  Max: {agg["time_max"]:.6f}s')

    @staticmethod
    def _std(values: List[float]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(var)

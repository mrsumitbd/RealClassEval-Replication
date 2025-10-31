from typing import List, Optional, Dict
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
        self._updates = 0
        self._total_sequences = 0
        self._total_length = 0
        self._total_bins = 0
        self._total_capacity_used = 0
        self._total_waste = 0
        self._total_overflow_amount = 0
        self._total_perfect_bins = 0
        self._total_empty_bins = 0

        # Derived averages (sum of per-update values to compute mean over updates)
        self._sum_avg_bin_utilization = 0.0
        self._sum_min_bin_utilization = 0.0
        self._sum_max_bin_utilization = 0.0
        self._sum_stdev_bin_utilization = 0.0
        self._sum_max_bin_imbalance = 0.0
        self._sum_avg_sequences_per_bin = 0.0
        self._sum_bin_count_ratio = 0.0
        self._feasible_count = 0

        # Time tracking
        self._sum_packing_time = 0.0
        self._count_packing_time = 0

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

        # Update aggregates
        self._updates += 1
        self._total_sequences += int(stats['total_sequences'])
        self._total_length += int(stats['total_length'])
        self._total_bins += int(stats['num_bins'])
        self._total_capacity_used += int(stats['total_capacity_used'])
        self._total_waste += int(stats['total_waste'])
        self._total_overflow_amount += int(stats['overflow_amount'])
        self._total_perfect_bins += int(stats['perfect_bins'])
        self._total_empty_bins += int(stats['empty_bins'])

        self._sum_avg_bin_utilization += stats['avg_bin_utilization']
        self._sum_min_bin_utilization += stats['min_bin_utilization']
        self._sum_max_bin_utilization += stats['max_bin_utilization']
        self._sum_stdev_bin_utilization += stats['stdev_bin_utilization']
        self._sum_max_bin_imbalance += stats['max_bin_imbalance']
        self._sum_avg_sequences_per_bin += stats['avg_sequences_per_bin']
        self._sum_bin_count_ratio += stats['bin_count_ratio']
        if stats['feasible'] >= 0.5:
            self._feasible_count += 1

        if packing_time is not None:
            self._sum_packing_time += float(packing_time)
            self._count_packing_time += 1
            stats['packing_time'] = float(packing_time)
        else:
            stats['packing_time'] = 0.0

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
        num_bins = len(bins)
        total_sequences = len(sequence_lengths)
        total_length = int(sum(int(x) for x in sequence_lengths))

        # Compute load per bin
        seq_len = sequence_lengths
        n_seq = len(seq_len)

        bin_loads: List[int] = []
        overflow_bins = 0
        overflow_amount = 0

        for b in bins:
            load = 0
            for idx in b:
                if 0 <= idx < n_seq:
                    load += int(seq_len[idx])
            bin_loads.append(load)
            if load > bin_capacity:
                overflow_bins += 1
                overflow_amount += load - bin_capacity

        # Utilization per bin
        utilizations: List[float] = []
        perfect_bins = 0
        empty_bins = 0
        for load in bin_loads:
            if bin_capacity > 0:
                util = load / float(bin_capacity)
            else:
                util = 0.0
            utilizations.append(util)
            if load == bin_capacity:
                perfect_bins += 1
            if load == 0:
                empty_bins += 1

        # Aggregate utilization stats
        if num_bins > 0:
            avg_util = sum(utilizations) / num_bins
            min_util = min(utilizations)
            max_util = max(utilizations)
            mean_util = avg_util
            var_util = sum((u - mean_util) **
                           2 for u in utilizations) / num_bins
            stdev_util = math.sqrt(var_util)
            max_imbalance = (max(bin_loads) - min(bin_loads)
                             ) if bin_loads else 0
            avg_seq_per_bin = total_sequences / float(num_bins)
        else:
            avg_util = 0.0
            min_util = 0.0
            max_util = 0.0
            stdev_util = 0.0
            max_imbalance = 0.0
            avg_seq_per_bin = 0.0

        total_capacity_used = num_bins * int(bin_capacity)
        total_waste = max(0, total_capacity_used - sum(bin_loads))
        waste_ratio = (
            total_waste / total_capacity_used) if total_capacity_used > 0 else 0.0

        # Efficiency and lower bound
        lower_bound_bins = math.ceil(
            total_length / float(bin_capacity)) if bin_capacity > 0 else 0
        bin_count_ratio = (num_bins / float(lower_bound_bins)
                           ) if lower_bound_bins > 0 else float('inf') if num_bins > 0 else 0.0
        packing_efficiency = (
            1.0 - waste_ratio) if total_capacity_used > 0 else 0.0

        feasible = 1.0 if overflow_bins == 0 else 0.0

        return {
            'num_bins': float(num_bins),
            'total_sequences': float(total_sequences),
            'total_length': float(total_length),
            'bin_capacity': float(bin_capacity),
            'total_capacity_used': float(total_capacity_used),
            'total_waste': float(total_waste),
            'waste_ratio': float(waste_ratio),
            'avg_bin_utilization': float(avg_util),
            'min_bin_utilization': float(min_util),
            'max_bin_utilization': float(max_util),
            'stdev_bin_utilization': float(stdev_util),
            'overflow_bins': float(overflow_bins),
            'overflow_amount': float(overflow_amount),
            'perfect_bins': float(perfect_bins),
            'empty_bins': float(empty_bins),
            'max_bin_imbalance': float(max_imbalance),
            'avg_sequences_per_bin': float(avg_seq_per_bin),
            'lower_bound_bins': float(lower_bound_bins),
            'bin_count_ratio': float(bin_count_ratio),
            'packing_efficiency': float(packing_efficiency),
            'feasible': float(feasible),
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self._updates == 0:
            return {
                'updates': 0.0,
                'total_sequences': 0.0,
                'total_length': 0.0,
                'total_bins': 0.0,
                'total_capacity_used': 0.0,
                'total_waste': 0.0,
                'overall_waste_ratio': 0.0,
                'overall_utilization': 0.0,
                'avg_bin_utilization_per_update': 0.0,
                'avg_min_bin_utilization_per_update': 0.0,
                'avg_max_bin_utilization_per_update': 0.0,
                'avg_stdev_bin_utilization_per_update': 0.0,
                'avg_max_bin_imbalance_per_update': 0.0,
                'avg_sequences_per_bin_per_update': 0.0,
                'avg_bin_count_ratio_per_update': 0.0,
                'feasible_fraction': 0.0,
                'perfect_bins_total': 0.0,
                'empty_bins_total': 0.0,
                'overflow_amount_total': 0.0,
                'avg_packing_time': 0.0,
                'avg_bins_per_update': 0.0,
            }

        overall_waste_ratio = (
            self._total_waste / self._total_capacity_used) if self._total_capacity_used > 0 else 0.0
        overall_utilization = 1.0 - overall_waste_ratio

        avg_time = (self._sum_packing_time /
                    self._count_packing_time) if self._count_packing_time > 0 else 0.0

        return {
            'updates': float(self._updates),
            'total_sequences': float(self._total_sequences),
            'total_length': float(self._total_length),
            'total_bins': float(self._total_bins),
            'total_capacity_used': float(self._total_capacity_used),
            'total_waste': float(self._total_waste),
            'overall_waste_ratio': float(overall_waste_ratio),
            'overall_utilization': float(overall_utilization),
            'avg_bin_utilization_per_update': float(self._sum_avg_bin_utilization / self._updates),
            'avg_min_bin_utilization_per_update': float(self._sum_min_bin_utilization / self._updates),
            'avg_max_bin_utilization_per_update': float(self._sum_max_bin_utilization / self._updates),
            'avg_stdev_bin_utilization_per_update': float(self._sum_stdev_bin_utilization / self._updates),
            'avg_max_bin_imbalance_per_update': float(self._sum_max_bin_imbalance / self._updates),
            'avg_sequences_per_bin_per_update': float(self._sum_avg_sequences_per_bin / self._updates),
            'avg_bin_count_ratio_per_update': float(self._sum_bin_count_ratio / self._updates),
            'feasible_fraction': float(self._feasible_count / self._updates),
            'perfect_bins_total': float(self._total_perfect_bins),
            'empty_bins_total': float(self._total_empty_bins),
            'overflow_amount_total': float(self._total_overflow_amount),
            'avg_packing_time': float(avg_time),
            'avg_bins_per_update': float(self._total_bins / self._updates),
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print(f"Updates: {int(stats['updates'])}")
        print(f"Total sequences: {int(stats['total_sequences'])}")
        print(f"Total length: {int(stats['total_length'])}")
        print(f"Total bins: {int(stats['total_bins'])}")
        print(f"Total capacity used: {int(stats['total_capacity_used'])}")
        print(f"Total waste: {int(stats['total_waste'])}")
        print(f"Overall utilization: {stats['overall_utilization']:.4f}")
        print(f"Overall waste ratio: {stats['overall_waste_ratio']:.4f}")
        print(
            f"Average bin utilization per update: {stats['avg_bin_utilization_per_update']:.4f}")
        print(
            f"Average min bin utilization per update: {stats['avg_min_bin_utilization_per_update']:.4f}")
        print(
            f"Average max bin utilization per update: {stats['avg_max_bin_utilization_per_update']:.4f}")
        print(
            f"Average stdev bin utilization per update: {stats['avg_stdev_bin_utilization_per_update']:.4f}")
        print(
            f"Average max bin imbalance per update: {stats['avg_max_bin_imbalance_per_update']:.4f}")
        print(
            f"Average sequences per bin per update: {stats['avg_sequences_per_bin_per_update']:.4f}")
        print(
            f"Average bin count ratio per update: {stats['avg_bin_count_ratio_per_update']:.4f}")
        print(f"Feasible fraction: {stats['feasible_fraction']:.4f}")
        print(f"Perfect bins total: {int(stats['perfect_bins_total'])}")
        print(f"Empty bins total: {int(stats['empty_bins_total'])}")
        print(f"Overflow amount total: {int(stats['overflow_amount_total'])}")
        print(f"Average packing time: {stats['avg_packing_time']:.6f} s")
        print(f"Average bins per update: {stats['avg_bins_per_update']:.4f}")

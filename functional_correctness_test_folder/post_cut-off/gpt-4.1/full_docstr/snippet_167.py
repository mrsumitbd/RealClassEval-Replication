
from typing import List, Dict, Optional


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
        self.total_packing_ops = 0
        self.total_bins_used = 0
        self.total_sequences = 0
        self.total_sequence_length = 0
        self.total_bin_capacity = 0
        self.total_waste = 0.0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
        self.packing_times = []

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        '''Update metrics with a new packing solution.'''
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_packing_ops += 1
        self.total_bins_used += stats['num_bins']
        self.total_sequences += len(sequence_lengths)
        self.total_sequence_length += sum(sequence_lengths)
        self.total_bin_capacity += stats['num_bins'] * bin_capacity
        self.total_waste += stats['waste']
        self.total_utilization += stats['utilization']
        self.total_imbalance += stats['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
            self.packing_times.append(packing_time)
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        '''Calculate metrics for a packing solution without updating the tracker.'''
        num_bins = len(bins)
        total_seq_len = sum(sequence_lengths)
        bin_usages = []
        for b in bins:
            usage = sum(sequence_lengths[i] for i in b)
            bin_usages.append(usage)
        total_bin_capacity = num_bins * bin_capacity
        waste = total_bin_capacity - total_seq_len
        utilization = total_seq_len / total_bin_capacity if total_bin_capacity > 0 else 0.0
        if bin_usages:
            max_usage = max(bin_usages)
            min_usage = min(bin_usages)
            imbalance = max_usage - min_usage
        else:
            imbalance = 0.0
        return {
            'num_bins': num_bins,
            'waste': float(waste),
            'utilization': float(utilization),
            'imbalance': float(imbalance)
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.'''
        if self.total_packing_ops == 0:
            return {
                'avg_num_bins': 0.0,
                'avg_waste': 0.0,
                'avg_utilization': 0.0,
                'avg_imbalance': 0.0,
                'avg_packing_time': 0.0,
                'total_packing_ops': 0
            }
        avg_num_bins = self.total_bins_used / self.total_packing_ops
        avg_waste = self.total_waste / self.total_packing_ops
        avg_utilization = self.total_utilization / self.total_packing_ops
        avg_imbalance = self.total_imbalance / self.total_packing_ops
        avg_packing_time = (self.total_packing_time /
                            len(self.packing_times)) if self.packing_times else 0.0
        return {
            'avg_num_bins': avg_num_bins,
            'avg_waste': avg_waste,
            'avg_utilization': avg_utilization,
            'avg_imbalance': avg_imbalance,
            'avg_packing_time': avg_packing_time,
            'total_packing_ops': self.total_packing_ops
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Total packing operations: {stats['total_packing_ops']}")
        print(f"  Average number of bins:   {stats['avg_num_bins']:.3f}")
        print(f"  Average waste:            {stats['avg_waste']:.3f}")
        print(f"  Average utilization:      {stats['avg_utilization']:.3f}")
        print(f"  Average imbalance:        {stats['avg_imbalance']:.3f}")
        print(
            f"  Average packing time:     {stats['avg_packing_time']:.6f} seconds")

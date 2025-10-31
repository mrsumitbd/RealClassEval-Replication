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
        self.num_updates = 0
        self.total_bins = 0
        self.total_sequences = 0
        self.total_capacity = 0
        self.total_used = 0
        self.total_waste = 0
        self.total_imbalance = 0
        self.total_utilization = 0.0
        self.total_packing_time = 0.0
        self.packing_times = []

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
        self.num_updates += 1
        self.total_bins += stats['num_bins']
        self.total_sequences += stats['num_sequences']
        self.total_capacity += stats['total_capacity']
        self.total_used += stats['total_used']
        self.total_waste += stats['total_waste']
        self.total_imbalance += stats['imbalance']
        self.total_utilization += stats['utilization']
        if packing_time is not None:
            self.total_packing_time += packing_time
            self.packing_times.append(packing_time)
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
        num_sequences = len(sequence_lengths)
        total_capacity = num_bins * bin_capacity
        bin_usages = []
        for b in bins:
            usage = sum(sequence_lengths[i] for i in b)
            bin_usages.append(usage)
        total_used = sum(bin_usages)
        total_waste = total_capacity - total_used
        utilization = total_used / total_capacity if total_capacity > 0 else 0.0
        if bin_usages:
            imbalance = max(bin_usages) - min(bin_usages)
        else:
            imbalance = 0.0
        stats = {
            'num_bins': float(num_bins),
            'num_sequences': float(num_sequences),
            'total_capacity': float(total_capacity),
            'total_used': float(total_used),
            'total_waste': float(total_waste),
            'utilization': utilization,
            'imbalance': float(imbalance),
        }
        return stats

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.num_updates == 0:
            return {
                'num_updates': 0.0,
                'avg_num_bins': 0.0,
                'avg_num_sequences': 0.0,
                'avg_total_capacity': 0.0,
                'avg_total_used': 0.0,
                'avg_total_waste': 0.0,
                'avg_utilization': 0.0,
                'avg_imbalance': 0.0,
                'avg_packing_time': 0.0,
                'min_packing_time': 0.0,
                'max_packing_time': 0.0,
            }
        avg_packing_time = self.total_packing_time / \
            self.num_updates if self.num_updates > 0 else 0.0
        min_packing_time = min(
            self.packing_times) if self.packing_times else 0.0
        max_packing_time = max(
            self.packing_times) if self.packing_times else 0.0
        return {
            'num_updates': float(self.num_updates),
            'avg_num_bins': self.total_bins / self.num_updates,
            'avg_num_sequences': self.total_sequences / self.num_updates,
            'avg_total_capacity': self.total_capacity / self.num_updates,
            'avg_total_used': self.total_used / self.num_updates,
            'avg_total_waste': self.total_waste / self.num_updates,
            'avg_utilization': self.total_utilization / self.num_updates,
            'avg_imbalance': self.total_imbalance / self.num_updates,
            'avg_packing_time': avg_packing_time,
            'min_packing_time': min_packing_time,
            'max_packing_time': max_packing_time,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Packing Metrics (Aggregated):")
        print(f"  Number of updates: {stats['num_updates']:.0f}")
        print(f"  Avg. number of bins: {stats['avg_num_bins']:.2f}")
        print(f"  Avg. number of sequences: {stats['avg_num_sequences']:.2f}")
        print(f"  Avg. total capacity: {stats['avg_total_capacity']:.2f}")
        print(f"  Avg. total used: {stats['avg_total_used']:.2f}")
        print(f"  Avg. total waste: {stats['avg_total_waste']:.2f}")
        print(f"  Avg. utilization: {stats['avg_utilization']*100:.2f}%")
        print(f"  Avg. imbalance: {stats['avg_imbalance']:.2f}")
        print(f"  Avg. packing time: {stats['avg_packing_time']:.6f} s")
        print(f"  Min. packing time: {stats['min_packing_time']:.6f} s")
        print(f"  Max. packing time: {stats['max_packing_time']:.6f} s")

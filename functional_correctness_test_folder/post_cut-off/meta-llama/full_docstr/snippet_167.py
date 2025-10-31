
from typing import List, Dict, Optional


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.total_bin_utilization = 0.0
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
        self.num_packing_operations = 0

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.total_bin_utilization = 0.0
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
        self.num_packing_operations = 0

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
        self.total_bin_utilization += stats['bin_utilization']
        self.total_waste += stats['waste']
        self.total_imbalance += stats['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_packing_operations += 1
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
        total_used = sum(sum(sequence_lengths[i] for i in bin) for bin in bins)
        total_capacity = len(bins) * bin_capacity
        bin_utilization = total_used / total_capacity if total_capacity > 0 else 0.0
        waste = 1.0 - bin_utilization
        bin_sizes = [sum(sequence_lengths[i] for i in bin) for bin in bins]
        avg_bin_size = sum(bin_sizes) / len(bin_sizes) if bin_sizes else 0.0
        imbalance = sum(abs(size - avg_bin_size)
                        for size in bin_sizes) / len(bin_sizes) if bin_sizes else 0.0
        return {
            'bin_utilization': bin_utilization,
            'waste': waste,
            'imbalance': imbalance,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.num_packing_operations == 0:
            return {
                'avg_bin_utilization': 0.0,
                'avg_waste': 0.0,
                'avg_imbalance': 0.0,
                'avg_packing_time': 0.0,
            }
        return {
            'avg_bin_utilization': self.total_bin_utilization / self.num_packing_operations,
            'avg_waste': self.total_waste / self.num_packing_operations,
            'avg_imbalance': self.total_imbalance / self.num_packing_operations,
            'avg_packing_time': self.total_packing_time / self.num_packing_operations,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Aggregated Metrics:")
        print(f"  Average Bin Utilization: {stats['avg_bin_utilization']:.4f}")
        print(f"  Average Waste: {stats['avg_waste']:.4f}")
        print(f"  Average Imbalance: {stats['avg_imbalance']:.4f}")
        print(
            f"  Average Packing Time: {stats['avg_packing_time']:.4f} seconds")

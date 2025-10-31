
from typing import List, Dict, Optional


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.total_packing_time = 0.0
        self.total_waste = 0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0
        self.num_packing_operations = 0

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.total_packing_time = 0.0
        self.total_waste = 0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0
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
        self.total_waste += stats['waste']
        self.total_utilization += stats['utilization']
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
        total_used_capacity = 0
        max_bin_usage = 0
        min_bin_usage = float('inf')
        for bin in bins:
            bin_usage = sum(sequence_lengths[i] for i in bin)
            total_used_capacity += bin_usage
            max_bin_usage = max(max_bin_usage, bin_usage)
            min_bin_usage = min(min_bin_usage, bin_usage)

        total_capacity = len(bins) * bin_capacity
        waste = total_capacity - total_used_capacity
        utilization = total_used_capacity / total_capacity if total_capacity > 0 else 0
        imbalance = max_bin_usage - min_bin_usage if len(bins) > 0 else 0

        return {
            'waste': waste,
            'utilization': utilization,
            'imbalance': imbalance
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.num_packing_operations == 0:
            return {
                'average_waste': 0,
                'average_utilization': 0,
                'average_imbalance': 0,
                'average_packing_time': 0
            }
        return {
            'average_waste': self.total_waste / self.num_packing_operations,
            'average_utilization': self.total_utilization / self.num_packing_operations,
            'average_imbalance': self.total_imbalance / self.num_packing_operations,
            'average_packing_time': self.total_packing_time / self.num_packing_operations if self.total_packing_time > 0 else 0
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print(f"Average Waste: {stats['average_waste']:.2f}")
        print(f"Average Utilization: {stats['average_utilization']:.2%}")
        print(f"Average Imbalance: {stats['average_imbalance']:.2f}")
        print(
            f"Average Packing Time: {stats['average_packing_time']:.4f} seconds")

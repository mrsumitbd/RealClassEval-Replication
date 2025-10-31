
from typing import List, Optional, Dict


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.total_packing_time = 0.0
        self.total_sequences = 0
        self.total_bins_used = 0
        self.total_waste = 0
        self.total_utilization = 0.0
        self.num_packing_operations = 0

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.total_packing_time = 0.0
        self.total_sequences = 0
        self.total_bins_used = 0
        self.total_waste = 0
        self.total_utilization = 0.0
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
        self.total_packing_time += packing_time if packing_time is not None else 0.0
        self.total_sequences += len(sequence_lengths)
        self.total_bins_used += len(bins)
        self.total_waste += stats['waste']
        self.total_utilization += stats['utilization']
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
        total_length = sum(sequence_lengths)
        total_bin_length = sum(
            sum(sequence_lengths[i] for i in bin) for bin in bins)
        waste = len(bins) * bin_capacity - total_bin_length
        utilization = total_bin_length / \
            (len(bins) * bin_capacity) if len(bins) > 0 else 0.0
        return {
            'waste': waste,
            'utilization': utilization,
            'imbalance': max(sum(sequence_lengths[i] for i in bin) for bin in bins) / (sum(sequence_lengths) / len(bins)) if len(bins) > 0 else 0.0
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.num_packing_operations == 0:
            return {
                'average_packing_time': 0.0,
                'average_utilization': 0.0,
                'average_waste': 0.0,
                'average_sequences_per_operation': 0.0,
                'average_bins_per_operation': 0.0
            }
        return {
            'average_packing_time': self.total_packing_time / self.num_packing_operations,
            'average_utilization': self.total_utilization / self.num_packing_operations,
            'average_waste': self.total_waste / self.num_packing_operations,
            'average_sequences_per_operation': self.total_sequences / self.num_packing_operations,
            'average_bins_per_operation': self.total_bins_used / self.num_packing_operations
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print(
            f"Average Packing Time: {stats['average_packing_time']:.4f} seconds")
        print(f"Average Utilization: {stats['average_utilization']:.4f}")
        print(f"Average Waste: {stats['average_waste']:.4f}")
        print(
            f"Average Sequences per Operation: {stats['average_sequences_per_operation']:.2f}")
        print(
            f"Average Bins per Operation: {stats['average_bins_per_operation']:.2f}")

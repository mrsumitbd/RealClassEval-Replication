
from typing import List, Dict, Optional


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.total_sequences = 0
        self.total_bins = 0
        self.total_bin_utilization = 0.0
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
        self.num_packing_operations = 0

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.total_sequences = 0
        self.total_bins = 0
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
        metrics = self.calculate_stats_only(
            sequence_lengths, bins, bin_capacity)
        self.total_sequences += len(sequence_lengths)
        self.total_bins += len(bins)
        self.total_bin_utilization += metrics['bin_utilization']
        self.total_waste += metrics['waste']
        self.total_imbalance += metrics['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_packing_operations += 1
        return metrics

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        '''Calculate metrics for a packing solution without updating the tracker.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
        Returns:
            Dictionary of metrics for this packing solution
        '''
        bin_utilizations = []
        bin_contents = []
        for bin_indices in bins:
            bin_content = sum(sequence_lengths[i] for i in bin_indices)
            bin_utilization = bin_content / bin_capacity
            bin_utilizations.append(bin_utilization)
            bin_contents.append(bin_content)

        avg_bin_utilization = sum(bin_utilizations) / len(bin_utilizations)
        waste = sum(bin_capacity - content for content in bin_contents)
        imbalance = max(bin_utilizations) - min(bin_utilizations)

        return {
            'bin_utilization': avg_bin_utilization,
            'waste': waste,
            'imbalance': imbalance
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
                'avg_packing_time': 0.0
            }

        return {
            'avg_bin_utilization': self.total_bin_utilization / self.num_packing_operations,
            'avg_waste': self.total_waste / self.num_packing_operations,
            'avg_imbalance': self.total_imbalance / self.num_packing_operations,
            'avg_packing_time': self.total_packing_time / self.num_packing_operations
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Average Bin Utilization: {stats['avg_bin_utilization']:.2%}")
        print(f"  Average Waste: {stats['avg_waste']:.2f}")
        print(f"  Average Imbalance: {stats['avg_imbalance']:.2%}")
        print(
            f"  Average Packing Time: {stats['avg_packing_time']:.2f} seconds")

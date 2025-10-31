
from typing import List, Dict, Optional
import numpy as np


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.total_packing_operations = 0
        self.total_sequences = 0
        self.total_bins = 0
        self.total_waste = 0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.total_packing_operations = 0
        self.total_sequences = 0
        self.total_bins = 0
        self.total_waste = 0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0

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

        self.total_packing_operations += 1
        self.total_sequences += len(sequence_lengths)
        self.total_bins += len(bins)
        self.total_waste += stats['total_waste']
        self.total_utilization += stats['avg_utilization']
        self.total_imbalance += stats['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time

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
        bin_utilizations = []
        for bin in bins:
            total = sum(sequence_lengths[i] for i in bin)
            utilization = total / bin_capacity
            bin_utilizations.append(utilization)

        avg_utilization = np.mean(
            bin_utilizations) if bin_utilizations else 0.0
        total_waste = sum((1 - u) * bin_capacity for u in bin_utilizations)
        imbalance = np.std(bin_utilizations) if bin_utilizations else 0.0

        return {
            'num_bins': len(bins),
            'num_sequences': len(sequence_lengths),
            'avg_utilization': avg_utilization,
            'total_waste': total_waste,
            'imbalance': imbalance,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        avg_utilization = self.total_utilization / \
            self.total_packing_operations if self.total_packing_operations > 0 else 0.0
        avg_imbalance = self.total_imbalance / \
            self.total_packing_operations if self.total_packing_operations > 0 else 0.0
        avg_packing_time = self.total_packing_time / \
            self.total_packing_operations if self.total_packing_operations > 0 else 0.0

        return {
            'total_packing_operations': self.total_packing_operations,
            'total_sequences': self.total_sequences,
            'total_bins': self.total_bins,
            'avg_utilization': avg_utilization,
            'total_waste': self.total_waste,
            'avg_imbalance': avg_imbalance,
            'avg_packing_time': avg_packing_time,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(
            f"  Total Packing Operations: {stats['total_packing_operations']}")
        print(f"  Total Sequences Packed: {stats['total_sequences']}")
        print(f"  Total Bins Used: {stats['total_bins']}")
        print(f"  Average Bin Utilization: {stats['avg_utilization']:.2%}")
        print(f"  Total Waste: {stats['total_waste']:.2f}")
        print(f"  Average Imbalance: {stats['avg_imbalance']:.4f}")
        print(
            f"  Average Packing Time: {stats['avg_packing_time']:.4f} seconds")

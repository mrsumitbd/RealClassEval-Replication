
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
        self.total_packing_time = 0.0
        self.total_bins_used = 0
        self.total_waste = 0.0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.total_packing_operations = 0
        self.total_packing_time = 0.0
        self.total_bins_used = 0
        self.total_waste = 0.0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0

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

        self.total_packing_operations += 1
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.total_bins_used += metrics['num_bins']
        self.total_waste += metrics['total_waste']
        self.total_utilization += metrics['avg_utilization']
        self.total_imbalance += metrics['imbalance']

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
        num_bins = len(bins)
        bin_utilizations = []
        total_waste = 0.0

        for bin_indices in bins:
            bin_sum = sum(sequence_lengths[i] for i in bin_indices)
            utilization = bin_sum / bin_capacity
            waste = bin_capacity - bin_sum
            bin_utilizations.append(utilization)
            total_waste += waste

        avg_utilization = np.mean(
            bin_utilizations) if bin_utilizations else 0.0
        imbalance = np.std(bin_utilizations) if bin_utilizations else 0.0

        return {
            'num_bins': num_bins,
            'total_waste': total_waste,
            'avg_utilization': avg_utilization,
            'imbalance': imbalance,
            'min_utilization': min(bin_utilizations) if bin_utilizations else 0.0,
            'max_utilization': max(bin_utilizations) if bin_utilizations else 0.0,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.total_packing_operations == 0:
            return {}

        return {
            'avg_packing_time': self.total_packing_time / self.total_packing_operations,
            'avg_bins_used': self.total_bins_used / self.total_packing_operations,
            'avg_waste': self.total_waste / self.total_packing_operations,
            'avg_utilization': self.total_utilization / self.total_packing_operations,
            'avg_imbalance': self.total_imbalance / self.total_packing_operations,
            'total_packing_operations': self.total_packing_operations,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        if not stats:
            print("No packing operations recorded.")
            return

        print("Aggregated Packing Metrics:")
        print(
            f"  Total packing operations: {stats['total_packing_operations']}")
        print(f"  Average bins used: {stats['avg_bins_used']:.2f}")
        print(f"  Average waste: {stats['avg_waste']:.2f}")
        print(f"  Average utilization: {stats['avg_utilization']:.2%}")
        print(f"  Average imbalance: {stats['avg_imbalance']:.4f}")
        if 'avg_packing_time' in stats:
            print(
                f"  Average packing time: {stats['avg_packing_time']:.4f} seconds")

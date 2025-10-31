
from typing import Dict, List, Optional
import numpy as np


class PackingMetrics:
    """Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    """

    def __init__(self):
        """Initialize the metrics tracker."""
        self._total_packing_time = 0.0
        self._total_packing_operations = 0
        self._total_bins_used = 0
        self._total_waste = 0.0
        self._total_utilization = 0.0
        self._total_imbalance = 0.0

    def reset(self) -> None:
        """Reset all metrics."""
        self._total_packing_time = 0.0
        self._total_packing_operations = 0
        self._total_bins_used = 0
        self._total_waste = 0.0
        self._total_utilization = 0.0
        self._total_imbalance = 0.0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        """Update metrics with a new packing solution.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
            packing_time: Optional time taken to compute the packing solution
        Returns:
            Dictionary of metrics for this packing solution
        """
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)

        if packing_time is not None:
            self._total_packing_time += packing_time
            stats['packing_time'] = packing_time

        self._total_packing_operations += 1
        self._total_bins_used += stats['num_bins']
        self._total_waste += stats['total_waste']
        self._total_utilization += stats['avg_utilization']
        self._total_imbalance += stats['imbalance']

        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        """Calculate metrics for a packing solution without updating the tracker.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
        Returns:
            Dictionary of metrics for this packing solution
        """
        num_bins = len(bins)
        bin_utilizations = []

        for bin_items in bins:
            bin_sum = sum(sequence_lengths[i] for i in bin_items)
            utilization = bin_sum / bin_capacity
            bin_utilizations.append(utilization)

        avg_utilization = np.mean(
            bin_utilizations) if bin_utilizations else 0.0
        total_waste = sum(1 - util for util in bin_utilizations)
        imbalance = np.std(bin_utilizations) if bin_utilizations else 0.0

        return {
            'num_bins': num_bins,
            'avg_utilization': avg_utilization,
            'total_waste': total_waste,
            'imbalance': imbalance,
            'min_utilization': min(bin_utilizations) if bin_utilizations else 0.0,
            'max_utilization': max(bin_utilizations) if bin_utilizations else 0.0
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        """Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        """
        if self._total_packing_operations == 0:
            return {}

        return {
            'avg_packing_time': self._total_packing_time / self._total_packing_operations,
            'avg_bins_used': self._total_bins_used / self._total_packing_operations,
            'avg_waste': self._total_waste / self._total_packing_operations,
            'avg_utilization': self._total_utilization / self._total_packing_operations,
            'avg_imbalance': self._total_imbalance / self._total_packing_operations,
            'total_packing_operations': self._total_packing_operations
        }

    def print_aggregated_stats(self) -> None:
        """Print the aggregated metrics in a formatted way."""
        stats = self.get_aggregated_stats()
        if not stats:
            print("No packing operations recorded.")
            return

        print("\nAggregated Packing Metrics:")
        print("---------------------------")
        print(f"Total packing operations: {stats['total_packing_operations']}")
        print(f"Average packing time: {stats['avg_packing_time']:.4f} seconds")
        print(f"Average bins used: {stats['avg_bins_used']:.2f}")
        print(f"Average waste: {stats['avg_waste']:.2%}")
        print(f"Average utilization: {stats['avg_utilization']:.2%}")
        print(f"Average imbalance: {stats['avg_imbalance']:.4f}")

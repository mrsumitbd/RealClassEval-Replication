
from typing import List, Dict, Optional


class PackingMetrics:
    """Class for tracking and computing metrics for sequence packing algorithms.

    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    """

    def __init__(self):
        """Initialize the metrics tracker."""
        self.total_bins = 0
        self.total_bin_capacity = 0
        self.total_used_capacity = 0
        self.total_waste = 0
        self.total_imbalance = 0
        self.total_packing_time = 0
        self.num_packing_operations = 0

    def reset(self) -> None:
        """Reset all metrics."""
        self.total_bins = 0
        self.total_bin_capacity = 0
        self.total_used_capacity = 0
        self.total_waste = 0
        self.total_imbalance = 0
        self.total_packing_time = 0
        self.num_packing_operations = 0

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
        self.total_bins += len(bins)
        self.total_bin_capacity += len(bins) * bin_capacity
        self.total_used_capacity += stats['used_capacity']
        self.total_waste += stats['waste']
        self.total_imbalance += stats['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_packing_operations += 1
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
        used_capacity = sum(min(bin_capacity, sum(
            sequence_lengths[i] for i in bin)) for bin in bins)
        waste = len(bins) * bin_capacity - used_capacity
        imbalance = max((sum(sequence_lengths[i] for i in bin) for bin in bins), default=0) - min(
            (sum(sequence_lengths[i] for i in bin) for bin in bins), default=0)
        return {
            'num_bins': len(bins),
            'bin_capacity': bin_capacity,
            'used_capacity': used_capacity,
            'waste': waste,
            'imbalance': imbalance,
            'utilization': used_capacity / (len(bins) * bin_capacity) if len(bins) > 0 else 0.0,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        """Get aggregated metrics across all packing operations.

        Returns:
            Dictionary of aggregated metrics
        """
        if self.num_packing_operations == 0:
            return {
                'avg_num_bins': 0.0,
                'avg_bin_capacity': 0.0,
                'avg_used_capacity': 0.0,
                'avg_waste': 0.0,
                'avg_imbalance': 0.0,
                'avg_utilization': 0.0,
                'avg_packing_time': 0.0,
            }
        return {
            'avg_num_bins': self.total_bins / self.num_packing_operations,
            'avg_bin_capacity': self.total_bin_capacity / self.num_packing_operations,
            'avg_used_capacity': self.total_used_capacity / self.num_packing_operations,
            'avg_waste': self.total_waste / self.num_packing_operations,
            'avg_imbalance': self.total_imbalance / self.num_packing_operations,
            'avg_utilization': self.total_used_capacity / self.total_bin_capacity,
            'avg_packing_time': self.total_packing_time / self.num_packing_operations,
        }

    def print_aggregated_stats(self) -> None:
        """Print the aggregated metrics in a formatted way."""
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Average Number of Bins: {stats['avg_num_bins']:.2f}")
        print(f"  Average Bin Capacity: {stats['avg_bin_capacity']:.2f}")
        print(f"  Average Used Capacity: {stats['avg_used_capacity']:.2f}")
        print(f"  Average Waste: {stats['avg_waste']:.2f}")
        print(f"  Average Imbalance: {stats['avg_imbalance']:.2f}")
        print(f"  Average Utilization: {stats['avg_utilization']:.4f}")
        print(
            f"  Average Packing Time: {stats['avg_packing_time']:.4f} seconds")

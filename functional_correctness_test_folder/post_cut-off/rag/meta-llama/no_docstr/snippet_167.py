
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
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
        self.num_packing_operations = 0

    def reset(self) -> None:
        """Reset all metrics."""
        self.total_bins = 0
        self.total_bin_capacity = 0
        self.total_used_capacity = 0
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
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
        self.total_used_capacity += sum(stats['used_capacity'])
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
        used_capacity = [sum(sequence_lengths[i] for i in bin) for bin in bins]
        waste = sum(bin_capacity - cap for cap in used_capacity)
        imbalance = max(used_capacity) - min(used_capacity)
        stats = {
            'num_bins': len(bins),
            'bin_capacity': bin_capacity,
            'used_capacity': used_capacity,
            'waste': waste,
            'imbalance': imbalance,
            'efficiency': sum(used_capacity) / (len(bins) * bin_capacity) if len(bins) > 0 else 0.0,
        }
        return stats

    def get_aggregated_stats(self) -> Dict[str, float]:
        """Get aggregated metrics across all packing operations.

        Returns:
            Dictionary of aggregated metrics
        """
        aggregated_stats = {
            'avg_num_bins': self.total_bins / self.num_packing_operations if self.num_packing_operations > 0 else 0.0,
            'avg_bin_utilization': self.total_used_capacity / self.total_bin_capacity if self.total_bin_capacity > 0 else 0.0,
            'avg_waste': self.total_waste / self.num_packing_operations if self.num_packing_operations > 0 else 0.0,
            'avg_imbalance': self.total_imbalance / self.num_packing_operations if self.num_packing_operations > 0 else 0.0,
            'avg_packing_time': self.total_packing_time / self.num_packing_operations if self.num_packing_operations > 0 else 0.0,
        }
        return aggregated_stats

    def print_aggregated_stats(self) -> None:
        """Print the aggregated metrics in a formatted way."""
        aggregated_stats = self.get_aggregated_stats()
        print("Aggregated Metrics:")
        print(
            f"Average Number of Bins: {aggregated_stats['avg_num_bins']:.2f}")
        print(
            f"Average Bin Utilization: {aggregated_stats['avg_bin_utilization'] * 100:.2f}%")
        print(f"Average Waste: {aggregated_stats['avg_waste']:.2f}")
        print(f"Average Imbalance: {aggregated_stats['avg_imbalance']:.2f}")
        print(
            f"Average Packing Time: {aggregated_stats['avg_packing_time']:.2f} seconds")

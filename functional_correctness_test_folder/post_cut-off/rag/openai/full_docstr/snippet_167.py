
from __future__ import annotations

from typing import Dict, List, Optional


class PackingMetrics:
    """Class for tracking and computing metrics for sequence packing algorithms.

    The metrics tracked are:
        * number of bins used
        * total number of sequences packed
        * total capacity used
        * total waste (unused capacity)
        * average bin utilization
        * imbalance (max load – min load) normalized by bin capacity
        * total packing time
        * aggregated statistics across multiple updates
    """

    def __init__(self) -> None:
        """Initialize the metrics tracker."""
        self.reset()

    def reset(self) -> None:
        """Reset all metrics."""
        # Aggregated totals
        self._total_bins: int = 0
        self._total_sequences: int = 0
        self._total_capacity_used: int = 0
        self._total_capacity_available: int = 0
        self._total_waste: int = 0
        self._total_utilization: float = 0.0
        self._total_imbalance: float = 0.0
        self._total_packing_time: float = 0.0
        self._count: int = 0

    def update(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int,
        packing_time: Optional[float] = None,
    ) -> Dict[str, float]:
        """Update metrics with a new packing solution.

        Args:
            sequence_lengths: List of sequence lengths.
            bins: List of bins, where each bin is a list of indices.
            bin_capacity: Maximum capacity of each bin.
            packing_time: Optional time taken to compute the packing solution.

        Returns:
            Dictionary of metrics for this packing solution.
        """
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        # Update aggregated totals
        self._total_bins += stats["num_bins"]
        self._total_sequences += stats["total_sequences"]
        self._total_capacity_used += stats["total_capacity_used"]
        self._total_capacity_available += stats["total_capacity_available"]
        self._total_waste += stats["waste"]
        self._total_utilization += stats["utilization"]
        self._total_imbalance += stats["imbalance"]
        self._total_packing_time += stats["packing_time"]
        self._count += 1
        return stats

    def calculate_stats_only(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int,
    ) -> Dict[str, float]:
        """Calculate metrics for a packing solution without updating the tracker.

        Args:
            sequence_lengths: List of sequence lengths.
            bins: List of bins, where each bin is a list of indices.
            bin_capacity: Maximum capacity of each bin.

        Returns:
            Dictionary of metrics for this packing solution.
        """
        # Compute loads per bin
        bin_loads = [sum(sequence_lengths[i] for i in bin_indices)
                     for bin_indices in bins]
        num_bins = len(bins)
        total_capacity_used = sum(bin_loads)
        total_capacity_available = bin_capacity * num_bins
        waste = total_capacity_available - total_capacity_used
        utilization = total_capacity_used / \
            total_capacity_available if total_capacity_available else 0.0
        # Imbalance: (max load – min load) / bin_capacity
        if bin_loads:
            max_load = max(bin_loads)
            min_load = min(bin_loads)
            imbalance = (max_load - min_load) / \
                bin_capacity if bin_capacity else 0.0
        else:
            imbalance = 0.0

        return {
            "num_bins": num_bins,
            "total_sequences": len(sequence_lengths),
            "total_capacity_used": total_capacity_used,
            "total_capacity_available": total_capacity_available,
            "waste": waste,
            "utilization": utilization,
            "imbalance": imbalance,
            "packing_time": 0.0,  # placeholder; will be overridden in update if provided
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        """Get aggregated metrics across all packing operations.

        Returns:
            Dictionary of aggregated metrics.
        """
        if self._count == 0:
            return {
                "avg_num_bins": 0.0,
                "avg_total_sequences": 0.0,
                "avg_capacity_used": 0.0,
                "avg_capacity_available": 0.0,
                "avg_waste": 0.0,
                "avg_utilization": 0.0,
                "avg_imbalance": 0.0,
                "avg_packing_time": 0.0,
                "overall_utilization": 0.0,
            }

        overall_utilization = (
            self._total_capacity_used / self._total_capacity_available
            if self._total_capacity_available
            else 0.0
        )
        return {
            "avg_num_bins": self._total_bins / self._count,
            "avg_total_sequences": self._total_sequences / self._count,
            "avg_capacity_used": self._total_capacity_used / self._count,
            "avg_capacity_available": self._total_capacity_available / self._count,
            "avg_waste": self._total_waste / self._count,
            "avg_utilization": self._total_utilization / self._count,
            "avg_imbalance": self._total_imbalance / self._count,
            "avg_packing_time": self._total_packing_time / self._count,
            "overall_utilization": overall_utilization,
        }

    def print_aggregated_stats(self) -> None:
        """Print the aggregated metrics in a formatted way."""
        stats = self.get_aggregated_stats()
        print("=== Aggregated Packing Metrics ===")
        print(f"Average number of bins used: {stats['avg_num_bins']:.2f}")
        print(
            f"Average total sequences packed: {stats['avg_total_sequences']:.2f}")
        print(f"Average capacity used: {stats['avg_capacity_used']:.2f}")
        print(
            f"Average capacity available: {stats['avg_capacity_available']:.2f}")
        print(f"Average waste: {stats['avg_waste']:.2f}")
        print(f"Average utilization: {stats['avg_utilization']:.4f}")
        print(f"Average imbalance: {stats['avg_imbalance']:.4f}")
        print(f"Average packing time: {stats['avg_packing_time']:.4f} s")
        print(
            f"Overall utilization across all packings: {stats['overall_utilization']:.4f}")

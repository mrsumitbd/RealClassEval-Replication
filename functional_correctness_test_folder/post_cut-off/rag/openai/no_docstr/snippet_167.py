
from __future__ import annotations

from typing import Dict, List, Optional
import math


class PackingMetrics:
    """Class for tracking and computing metrics for sequence packing algorithms.

    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    """

    def __init__(self) -> None:
        """Initialize the metrics tracker."""
        self.reset()

    def reset(self) -> None:
        """Reset all metrics."""
        # Aggregated totals
        self._total_bins_used: int = 0
        self._total_utilization: float = 0.0
        self._total_waste: float = 0.0
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
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
            packing_time: Optional time taken to compute the packing solution

        Returns:
            Dictionary of metrics for this packing solution
        """
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        # Update aggregated totals
        self._total_bins_used += stats["bins_used"]
        self._total_utilization += stats["average_utilization"]
        self._total_waste += stats["average_waste"]
        self._total_imbalance += stats["average_imbalance"]
        self._total_packing_time += packing_time or 0.0
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
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin

        Returns:
            Dictionary of metrics for this packing solution
        """
        if not bins:
            return {
                "bins_used": 0,
                "average_utilization": 0.0,
                "average_waste": 0.0,
                "average_imbalance": 0.0,
            }

        # Compute usage per bin
        usages = []
        for bin_indices in bins:
            usage = sum(sequence_lengths[i] for i in bin_indices)
            usages.append(usage)

        # Utilization per bin
        utilizations = [u / bin_capacity for u in usages]
        average_utilization = sum(utilizations) / len(utilizations)

        # Waste per bin
        wastes = [bin_capacity - u for u in usages]
        average_waste = sum(wastes) / len(wastes)

        # Imbalance: max usage - min usage
        imbalance = max(usages) - min(usages) if usages else 0.0

        return {
            "bins_used": len(bins),
            "average_utilization": average_utilization,
            "average_waste": average_waste,
            "average_imbalance": imbalance,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        """Get aggregated metrics across all packing operations.

        Returns:
            Dictionary of aggregated metrics
        """
        if self._count == 0:
            return {
                "average_bins_used": 0.0,
                "average_utilization": 0.0,
                "average_waste": 0.0,
                "average_imbalance": 0.0,
                "average_packing_time": 0.0,
            }

        return {
            "average_bins_used": self._total_bins_used / self._count,
            "average_utilization": self._total_utilization / self._count,
            "average_waste": self._total_waste / self._count,
            "average_imbalance": self._total_imbalance / self._count,
            "average_packing_time": self._total_packing_time / self._count,
        }

    def print_aggregated_stats(self) -> None:
        """Print the aggregated metrics in a formatted way."""
        stats = self.get_aggregated_stats()
        print("=== Aggregated Packing Metrics ===")
        print(f"Average bins used: {stats['average_bins_used']:.2f}")
        print(
            f"Average utilization: {stats['average_utilization'] * 100:.2f}%")
        print(f"Average waste: {stats['average_waste']:.2f} units")
        print(f"Average imbalance: {stats['average_imbalance']:.2f} units")
        print(f"Average packing time: {stats['average_packing_time']:.4f} s")

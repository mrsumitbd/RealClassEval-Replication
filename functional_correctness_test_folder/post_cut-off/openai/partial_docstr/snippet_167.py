
from typing import List, Dict, Optional
import math
import sys


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        """Reset all aggregated statistics."""
        self._agg_stats: Dict[str, float] = {
            'utilization': 0.0,
            'waste': 0.0,
            'imbalance': 0.0,
            'num_bins': 0,
            'total_sequences': 0,
            'total_length': 0,
            'packing_time': 0.0,
        }
        self._count: int = 0

    def update(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int,
        packing_time: Optional[float] = None
    ) -> Dict[str, float]:
        """Update aggregated statistics with a new packing result.

        Parameters
        ----------
        sequence_lengths : List[int]
            List of lengths of all sequences that were packed.
        bins : List[List[int]]
            List of bins, each bin is a list of sequence indices or lengths.
        bin_capacity : int
            Capacity of each bin.
        packing_time : Optional[float]
            Time taken to perform the packing (seconds). If None, time is not recorded.

        Returns
        -------
        Dict[str, float]
            Dictionary of metrics for this particular packing.
        """
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        if packing_time is not None:
            stats['packing_time'] = packing_time
        # Aggregate
        for key, value in stats.items():
            if key in self._agg_stats:
                self._agg_stats[key] += value
        self._count += 1
        return stats

    def calculate_stats_only(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int
    ) -> Dict[str, float]:
        """Calculate metrics for a single packing result without updating aggregates.

        Parameters
        ----------
        sequence_lengths : List[int]
            List of lengths of all sequences that were packed.
        bins : List[List[int]]
            List of bins, each bin is a list of sequence indices or lengths.
        bin_capacity : int
            Capacity of each bin.

        Returns
        -------
        Dict[str, float]
            Dictionary of metrics for this particular packing.
        """
        if bin_capacity <= 0:
            raise ValueError("bin_capacity must be positive")

        num_bins = len(bins)
        if num_bins == 0:
            return {
                'utilization': 0.0,
                'waste': 0.0,
                'imbalance': 0.0,
                'num_bins': 0,
                'total_sequences': 0,
                'total_length': 0,
                'packing_time': 0.0,
            }

        # Compute load per bin
        loads = []
        for bin_ in bins:
            # bin_ may contain indices or lengths; assume lengths
            load = sum(bin_)
            if load > bin_capacity:
                # Overfull bin: treat as full capacity for utilization
                load = bin_capacity
            loads.append(load)

        total_used = sum(loads)
        total_capacity = num_bins * bin_capacity
        utilization = total_used / total_capacity
        waste = 1.0 - utilization

        # Imbalance: coefficient of variation (std / mean)
        mean_load = total_used / num_bins
        if mean_load == 0:
            imbalance = 0.0
        else:
            variance = sum((l - mean_load) ** 2 for l in loads) / num_bins
            std_dev = math.sqrt(variance)
            imbalance = std_dev / mean_load

        total_sequences = len(sequence_lengths)
        total_length = sum(sequence_lengths)

        return {
            'utilization': utilization,
            'waste': waste,
            'imbalance': imbalance,
            'num_bins': num_bins,
            'total_sequences': total_sequences,
            'total_length': total_length,
            'packing_time': 0.0,  # placeholder; user may supply actual time
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        """Return the average aggregated statistics over all updates.

        Returns
        -------
        Dict[str, float]
            Dictionary of averaged metrics.
        """
        if self._count == 0:
            return {k: 0.0 for k in self._agg_stats}
        return {k: v / self._count for k, v in self._agg_stats.items()}

    def print_aggregated_stats(self) -> None:
        """Print the aggregated statistics in a readable format."""
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        for key, value in stats.items():
            if key in ('utilization', 'waste', 'imbalance'):
                print(f"  {key:12s}: {value:.4f}")
            else:
                print(f"  {key:12s}: {value:.0f}")

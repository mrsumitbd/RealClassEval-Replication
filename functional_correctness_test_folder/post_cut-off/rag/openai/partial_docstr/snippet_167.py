
from __future__ import annotations

from typing import Dict, List, Optional


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.reset()

    def reset(self) -> None:
        '''Reset all metrics.'''
        # Aggregated counters
        self._total_bins_used: int = 0
        self._total_bin_capacity: int = 0
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
        # Update aggregated totals
        self._total_bins_used += stats['bins_used']
        self._total_bin_capacity += stats['total_capacity']
        self._total_waste += stats['waste']
        self._total_utilization += stats['utilization']
        self._total_imbalance += stats['imbalance']
        if packing_time is not None:
            self._total_packing_time += packing_time
        self._count += 1
        # Include packing_time in returned dict if provided
        if packing_time is not None:
            stats['packing_time'] = packing_time
        return stats

    def calculate_stats_only(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int,
    ) -> Dict[str, float]:
        '''Calculate metrics for a packing solution without updating the tracker.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
        Returns:
            Dictionary of metrics for this packing solution
        '''
        if not bins:
            return {
                'bins_used': 0,
                'total_length': 0,
                'total_capacity': 0,
                'waste': 0,
                'utilization': 0.0,
                'imbalance': 0.0,
            }

        bin_usages = []
        for bin_indices in bins:
            usage = sum(sequence_lengths[i] for i in bin_indices)
            bin_usages.append(usage)

        bins_used = len(bins)
        total_length = sum(bin_usages)
        total_capacity = bins_used * bin_capacity
        waste = total_capacity - total_length
        utilization = total_length / total_capacity if total_capacity else 0.0
        # Imbalance: (max - min) / bin_capacity
        max_usage = max(bin_usages)
        min_usage = min(bin_usages)
        imbalance = (max_usage - min_usage) / \
            bin_capacity if bin_capacity else 0.0

        return {
            'bins_used': bins_used,
            'total_length': total_length,
            'total_capacity': total_capacity,
            'waste': waste,
            'utilization': utilization,
            'imbalance': imbalance,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self._count == 0:
            return {
                'avg_bins_used': 0.0,
                'avg_total_length': 0.0,
                'avg_total_capacity': 0.0,
                'avg_waste': 0.0,
                'avg_utilization': 0.0,
                'avg_imbalance': 0.0,
                'avg_packing_time': 0.0,
            }

        avg_bins_used = self._total_bins_used / self._count
        avg_total_length = self._total_bin_capacity - self._total_waste
        avg_total_capacity = self._total_bin_capacity
        avg_waste = self._total_waste / self._count
        avg_utilization = self._total_utilization / self._count
        avg_imbalance = self._total_imbalance / self._count
        avg_packing_time = self._total_packing_time / self._count

        return {
            'avg_bins_used': avg_bins_used,
            'avg_total_length': avg_total_length,
            'avg_total_capacity': avg_total_capacity,
            'avg_waste': avg_waste,
            'avg_utilization': avg_utilization,
            'avg_imbalance': avg_imbalance,
            'avg_packing_time': avg_packing_time,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Average bins used:          {stats['avg_bins_used']:.2f}")
        print(f"  Average total length:       {stats['avg_total_length']:.2f}")
        print(
            f"  Average total capacity:     {stats['avg_total_capacity']:.2f}")
        print(f"  Average waste:              {stats['avg_waste']:.2f}")
        print(f"  Average utilization:        {stats['avg_utilization']:.4f}")
        print(f"  Average imbalance:          {stats['avg_imbalance']:.4f}")
        print(f"  Average packing time (s):   {stats['avg_packing_time']:.4f}")

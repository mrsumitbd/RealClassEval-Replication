
from typing import List, Dict, Optional
import math


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
        self.num_updates = 0
        self.total_utilization = 0.0
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_bins_used = 0
        self.total_capacity_used = 0
        self.total_packing_time = 0.0

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
        stats = self.calculate_stats_only(
            sequence_lengths, bins, bin_capacity
        )
        if packing_time is not None:
            stats["packing_time"] = packing_time

        # Aggregate
        self.num_updates += 1
        self.total_utilization += stats["utilization"]
        self.total_waste += stats["waste"]
        self.total_imbalance += stats["imbalance"]
        self.total_bins_used += stats["num_bins_used"]
        self.total_capacity_used += stats["total_capacity_used"]
        if packing_time is not None:
            self.total_packing_time += packing_time

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
        # Compute load per bin
        loads = []
        for bin_indices in bins:
            load = sum(sequence_lengths[i] for i in bin_indices)
            loads.append(load)

        num_bins_used = len(bins)
        total_capacity_used = sum(loads)
        total_capacity = bin_capacity * num_bins_used

        utilization = (
            total_capacity_used / total_capacity if total_capacity > 0 else 0.0
        )
        waste = (
            (total_capacity - total_capacity_used) / total_capacity
            if total_capacity > 0
            else 0.0
        )

        # Imbalance: coefficient of variation (std / mean)
        if loads:
            mean_load = total_capacity_used / num_bins_used
            if mean_load > 0:
                variance = sum((l - mean_load) **
                               2 for l in loads) / num_bins_used
                std_dev = math.sqrt(variance)
                imbalance = std_dev / mean_load
            else:
                imbalance = 0.0
        else:
            imbalance = 0.0

        return {
            "num_bins_used": num_bins_used,
            "total_capacity_used": total_capacity_used,
            "total_capacity": total_capacity,
            "utilization": utilization,
            "waste": waste,
            "imbalance": imbalance,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.num_updates == 0:
            return {
                "avg_num_bins_used": 0.0,
                "avg_total_capacity_used": 0.0,
                "avg_utilization": 0.0,
                "avg_waste": 0.0,
                "avg_imbalance": 0.0,
                "avg_packing_time": 0.0,
            }

        avg_num_bins_used = self.total_bins_used / self.num_updates
        avg_total_capacity_used = self.total_capacity_used / self.num_updates
        avg_utilization = self.total_utilization / self.num_updates
        avg_waste = self.total_waste / self.num_updates
        avg_imbalance = self.total_imbalance / self.num_updates
        avg_packing_time = self.total_packing_time / self.num_updates

        return {
            "avg_num_bins_used": avg_num_bins_used,
            "avg_total_capacity_used": avg_total_capacity_used,
            "avg_utilization": avg_utilization,
            "avg_waste": avg_waste,
            "avg_imbalance": avg_imbalance,
            "avg_packing_time": avg_packing_time,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Average bins used: {stats['avg_num_bins_used']:.2f}")
        print(
            f"  Average capacity used: {stats['avg_total_capacity_used']:.2f}"
        )
        print(f"  Average utilization: {stats['avg_utilization']:.4f}")
        print(f"  Average waste: {stats['avg_waste']:.4f}")
        print(f"  Average imbalance: {stats['avg_imbalance']:.4f}")
        print(f"  Average packing time: {stats['avg_packing_time']:.4f} s")


from typing import List, Dict, Optional
import numpy as np


class PackingMetrics:

    def __init__(self):
        self.total_bins = 0
        self.total_items = 0
        self.total_packing_time = 0.0
        self.total_wasted_space = 0
        self.total_runs = 0

    def reset(self) -> None:
        self.total_bins = 0
        self.total_items = 0
        self.total_packing_time = 0.0
        self.total_wasted_space = 0
        self.total_runs = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)

        self.total_bins += len(bins)
        self.total_items += len(sequence_lengths)
        self.total_wasted_space += stats['wasted_space']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.total_runs += 1

        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        num_bins = len(bins)
        num_items = len(sequence_lengths)
        bin_utilization = [sum(bin) / bin_capacity for bin in bins]
        avg_utilization = np.mean(bin_utilization) if num_bins > 0 else 0.0
        wasted_space = sum(bin_capacity - sum(bin) for bin in bins)

        return {
            'num_bins': num_bins,
            'num_items': num_items,
            'avg_utilization': avg_utilization,
            'wasted_space': wasted_space,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        avg_bins = self.total_bins / self.total_runs if self.total_runs > 0 else 0.0
        avg_items = self.total_items / self.total_runs if self.total_runs > 0 else 0.0
        avg_wasted_space = self.total_wasted_space / \
            self.total_runs if self.total_runs > 0 else 0.0
        avg_packing_time = self.total_packing_time / \
            self.total_runs if self.total_runs > 0 else 0.0

        return {
            'avg_bins_per_run': avg_bins,
            'avg_items_per_run': avg_items,
            'avg_wasted_space_per_run': avg_wasted_space,
            'avg_packing_time_per_run': avg_packing_time,
            'total_runs': self.total_runs,
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Average bins per run: {stats['avg_bins_per_run']:.2f}")
        print(f"  Average items per run: {stats['avg_items_per_run']:.2f}")
        print(
            f"  Average wasted space per run: {stats['avg_wasted_space_per_run']:.2f}")
        print(
            f"  Average packing time per run: {stats['avg_packing_time_per_run']:.4f} sec")
        print(f"  Total runs: {stats['total_runs']}")

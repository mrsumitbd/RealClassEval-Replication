
from typing import List, Dict, Optional
import numpy as np


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        self.total_bins = 0
        self.total_items = 0
        self.total_packing_time = 0.0
        self.total_waste = 0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0
        self.num_updates = 0

    def reset(self) -> None:
        self.total_bins = 0
        self.total_items = 0
        self.total_packing_time = 0.0
        self.total_waste = 0
        self.total_utilization = 0.0
        self.total_imbalance = 0.0
        self.num_updates = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)

        self.total_bins += len(bins)
        self.total_items += len(sequence_lengths)
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.total_waste += stats['total_waste']
        self.total_utilization += stats['avg_utilization']
        self.total_imbalance += stats['imbalance']
        self.num_updates += 1

        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        num_bins = len(bins)
        total_items = len(sequence_lengths)

        utilizations = []
        for bin in bins:
            bin_sum = sum(bin)
            utilizations.append(bin_sum / bin_capacity)

        avg_utilization = np.mean(utilizations) if num_bins > 0 else 0.0
        total_waste = sum(bin_capacity - sum(bin) for bin in bins)

        std_utilization = np.std(utilizations) if num_bins > 0 else 0.0

        return {
            'num_bins': num_bins,
            'num_items': total_items,
            'avg_utilization': avg_utilization,
            'std_utilization': std_utilization,
            'total_waste': total_waste,
            'imbalance': std_utilization
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        avg_utilization = self.total_utilization / \
            self.num_updates if self.num_updates > 0 else 0.0
        avg_imbalance = self.total_imbalance / \
            self.num_updates if self.num_updates > 0 else 0.0
        avg_waste = self.total_waste / self.num_updates if self.num_updates > 0 else 0.0
        avg_packing_time = self.total_packing_time / \
            self.num_updates if self.num_updates > 0 else 0.0

        return {
            'total_bins': self.total_bins,
            'total_items': self.total_items,
            'avg_utilization': avg_utilization,
            'avg_imbalance': avg_imbalance,
            'avg_waste': avg_waste,
            'avg_packing_time': avg_packing_time
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"Total bins used: {stats['total_bins']}")
        print(f"Total items packed: {stats['total_items']}")
        print(f"Average bin utilization: {stats['avg_utilization']:.4f}")
        print(
            f"Average imbalance (std of utilizations): {stats['avg_imbalance']:.4f}")
        print(f"Average waste per update: {stats['avg_waste']:.2f}")
        if 'avg_packing_time' in stats:
            print(
                f"Average packing time per update: {stats['avg_packing_time']:.6f} sec")

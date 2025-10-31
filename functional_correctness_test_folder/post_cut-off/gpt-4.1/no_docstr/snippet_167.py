
from typing import List, Optional, Dict


class PackingMetrics:

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.total_bins = 0
        self.total_items = 0
        self.total_capacity = 0
        self.total_used = 0
        self.total_unused = 0
        self.total_packing_time = 0.0
        self.num_updates = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_bins += stats['num_bins']
        self.total_items += stats['num_items']
        self.total_capacity += stats['total_capacity']
        self.total_used += stats['total_used']
        self.total_unused += stats['total_unused']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_updates += 1
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        num_bins = len(bins)
        num_items = len(sequence_lengths)
        total_capacity = num_bins * bin_capacity
        used = 0
        for b in bins:
            used += sum(sequence_lengths[i] for i in b)
        unused = total_capacity - used
        stats = {
            'num_bins': num_bins,
            'num_items': num_items,
            'total_capacity': total_capacity,
            'total_used': used,
            'total_unused': unused,
            'avg_bin_utilization': (used / total_capacity) if total_capacity > 0 else 0.0,
            'avg_items_per_bin': (num_items / num_bins) if num_bins > 0 else 0.0
        }
        return stats

    def get_aggregated_stats(self) -> Dict[str, float]:
        if self.num_updates == 0:
            return {
                'avg_num_bins': 0.0,
                'avg_num_items': 0.0,
                'avg_total_capacity': 0.0,
                'avg_total_used': 0.0,
                'avg_total_unused': 0.0,
                'avg_bin_utilization': 0.0,
                'avg_items_per_bin': 0.0,
                'avg_packing_time': 0.0
            }
        avg_bin_utilization = (
            self.total_used / self.total_capacity) if self.total_capacity > 0 else 0.0
        avg_items_per_bin = (self.total_items /
                             self.total_bins) if self.total_bins > 0 else 0.0
        return {
            'avg_num_bins': self.total_bins / self.num_updates,
            'avg_num_items': self.total_items / self.num_updates,
            'avg_total_capacity': self.total_capacity / self.num_updates,
            'avg_total_used': self.total_used / self.num_updates,
            'avg_total_unused': self.total_unused / self.num_updates,
            'avg_bin_utilization': avg_bin_utilization,
            'avg_items_per_bin': avg_items_per_bin,
            'avg_packing_time': self.total_packing_time / self.num_updates if self.total_packing_time > 0 else 0.0
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        for k, v in stats.items():
            print(f"  {k}: {v:.4f}")

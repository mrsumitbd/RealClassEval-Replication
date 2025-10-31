
from typing import List, Dict, Optional


class PackingMetrics:

    def __init__(self):
        self.total_items = 0
        self.total_bins = 0
        self.total_waste = 0.0
        self.total_packing_time = 0.0
        self.num_packing_calls = 0

    def reset(self) -> None:
        self.total_items = 0
        self.total_bins = 0
        self.total_waste = 0.0
        self.total_packing_time = 0.0
        self.num_packing_calls = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_items += sum(sequence_lengths)
        self.total_bins += len(bins)
        self.total_waste += stats['waste'] * len(sequence_lengths)
        if packing_time is not None:
            self.total_packing_time += packing_time
            self.num_packing_calls += 1
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        total_item_size = sum(sequence_lengths)
        total_used_space = sum(sum(bin) for bin in bins)
        waste = (len(bins) * bin_capacity) - total_used_space
        waste_ratio = waste / total_item_size if total_item_size > 0 else 0.0
        num_items = len(sequence_lengths)
        num_bins = len(bins)
        return {
            'waste_ratio': waste_ratio,
            'num_items': num_items,
            'num_bins': num_bins,
            'waste': waste,
            'total_item_size': total_item_size,
            'total_used_space': total_used_space,
            'bin_capacity': bin_capacity
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        if self.total_items == 0:
            return {
                'average_waste_ratio': 0.0,
                'average_packing_time': 0.0
            }
        average_waste_ratio = self.total_waste / self.total_items
        average_packing_time = self.total_packing_time / \
            self.num_packing_calls if self.num_packing_calls > 0 else 0.0
        return {
            'average_waste_ratio': average_waste_ratio,
            'average_packing_time': average_packing_time,
            'total_items': self.total_items,
            'total_bins': self.total_bins
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"Average Waste Ratio: {stats['average_waste_ratio']:.4f}")
        print(
            f"Average Packing Time: {stats['average_packing_time']:.4f} seconds")
        print(f"Total Items: {stats.get('total_items', 0)}")
        print(f"Total Bins: {stats.get('total_bins', 0)}")

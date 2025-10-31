
from typing import List, Optional, Dict


class PackingMetrics:

    def __init__(self):
        self.total_packing_time = 0.0
        self.total_items = 0
        self.total_bins_used = 0
        self.total_wasted_space = 0
        self.total_packing_calls = 0

    def reset(self) -> None:
        self.total_packing_time = 0.0
        self.total_items = 0
        self.total_bins_used = 0
        self.total_wasted_space = 0
        self.total_packing_calls = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_packing_time += packing_time if packing_time is not None else 0.0
        self.total_items += sum(sequence_lengths)
        self.total_bins_used += len(bins)
        self.total_wasted_space += stats['wasted_space']
        self.total_packing_calls += 1
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        total_items = sum(sequence_lengths)
        total_bins_used = len(bins)
        used_space = sum(sum(bin) for bin in bins)
        wasted_space = total_bins_used * bin_capacity - used_space
        packing_efficiency = used_space / \
            (total_bins_used * bin_capacity) if total_bins_used > 0 else 0.0
        return {
            'total_items': total_items,
            'total_bins_used': total_bins_used,
            'used_space': used_space,
            'wasted_space': wasted_space,
            'packing_efficiency': packing_efficiency
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        if self.total_packing_calls == 0:
            return {
                'average_packing_time': 0.0,
                'average_items_per_call': 0.0,
                'average_bins_used_per_call': 0.0,
                'average_wasted_space_per_call': 0.0,
                'overall_packing_efficiency': 0.0
            }
        average_packing_time = self.total_packing_time / self.total_packing_calls
        average_items_per_call = self.total_items / self.total_packing_calls
        average_bins_used_per_call = self.total_bins_used / self.total_packing_calls
        average_wasted_space_per_call = self.total_wasted_space / self.total_packing_calls
        overall_packing_efficiency = (
            self.total_items / (self.total_bins_used * bin_capacity)) if self.total_bins_used > 0 else 0.0
        return {
            'average_packing_time': average_packing_time,
            'average_items_per_call': average_items_per_call,
            'average_bins_used_per_call': average_bins_used_per_call,
            'average_wasted_space_per_call': average_wasted_space_per_call,
            'overall_packing_efficiency': overall_packing_efficiency
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print(
            f"Average Packing Time: {stats['average_packing_time']:.4f} seconds")
        print(f"Average Items per Call: {stats['average_items_per_call']:.2f}")
        print(
            f"Average Bins Used per Call: {stats['average_bins_used_per_call']:.2f}")
        print(
            f"Average Wasted Space per Call: {stats['average_wasted_space_per_call']:.2f}")
        print(
            f"Overall Packing Efficiency: {stats['overall_packing_efficiency']:.2%}")

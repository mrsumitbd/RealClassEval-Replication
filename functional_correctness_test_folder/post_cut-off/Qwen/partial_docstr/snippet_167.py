
from typing import List, Optional, Dict


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        self.total_sequences = 0
        self.total_bins = 0
        self.total_waste = 0
        self.total_packing_time = 0.0
        self.max_bin_utilization = 0.0
        self.min_bin_utilization = 1.0
        self.total_bin_utilization = 0.0

    def reset(self) -> None:
        self.total_sequences = 0
        self.total_bins = 0
        self.total_waste = 0
        self.total_packing_time = 0.0
        self.max_bin_utilization = 0.0
        self.min_bin_utilization = 1.0
        self.total_bin_utilization = 0.0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_sequences += len(sequence_lengths)
        self.total_bins += len(bins)
        self.total_waste += stats['waste']
        self.total_bin_utilization += stats['average_bin_utilization']
        self.max_bin_utilization = max(
            self.max_bin_utilization, stats['max_bin_utilization'])
        self.min_bin_utilization = min(
            self.min_bin_utilization, stats['min_bin_utilization'])
        if packing_time is not None:
            self.total_packing_time += packing_time
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        total_waste = 0
        max_utilization = 0.0
        min_utilization = 1.0
        total_utilization = 0.0

        for bin in bins:
            bin_sum = sum(bin)
            utilization = bin_sum / bin_capacity
            total_waste += bin_capacity - bin_sum
            max_utilization = max(max_utilization, utilization)
            min_utilization = min(min_utilization, utilization)
            total_utilization += utilization

        average_utilization = total_utilization / len(bins) if bins else 0.0
        return {
            'waste': total_waste,
            'average_bin_utilization': average_utilization,
            'max_bin_utilization': max_utilization,
            'min_bin_utilization': min_utilization
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        average_bin_utilization = self.total_bin_utilization / \
            self.total_bins if self.total_bins else 0.0
        return {
            'total_sequences': self.total_sequences,
            'total_bins': self.total_bins,
            'total_waste': self.total_waste,
            'average_bin_utilization': average_bin_utilization,
            'max_bin_utilization': self.max_bin_utilization,
            'min_bin_utilization': self.min_bin_utilization,
            'total_packing_time': self.total_packing_time
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print(f"Total Sequences: {stats['total_sequences']}")
        print(f"Total Bins: {stats['total_bins']}")
        print(f"Total Waste: {stats['total_waste']}")
        print(
            f"Average Bin Utilization: {stats['average_bin_utilization']:.2f}")
        print(f"Max Bin Utilization: {stats['max_bin_utilization']:.2f}")
        print(f"Min Bin Utilization: {stats['min_bin_utilization']:.2f}")
        print(f"Total Packing Time: {stats['total_packing_time']:.2f} seconds")

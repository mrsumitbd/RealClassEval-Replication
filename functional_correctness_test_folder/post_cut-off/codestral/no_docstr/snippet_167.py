
from typing import List, Dict, Optional


class PackingMetrics:

    def __init__(self):
        self.total_sequences = 0
        self.total_bins = 0
        self.total_bin_capacity = 0
        self.total_packing_time = 0.0
        self.total_sequence_length = 0
        self.total_wasted_space = 0
        self.total_sequences_per_bin = 0
        self.total_bin_utilization = 0.0

    def reset(self) -> None:
        self.total_sequences = 0
        self.total_bins = 0
        self.total_bin_capacity = 0
        self.total_packing_time = 0.0
        self.total_sequence_length = 0
        self.total_wasted_space = 0
        self.total_sequences_per_bin = 0
        self.total_bin_utilization = 0.0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_sequences += len(sequence_lengths)
        self.total_bins += len(bins)
        self.total_bin_capacity += bin_capacity * len(bins)
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.total_sequence_length += sum(sequence_lengths)
        self.total_wasted_space += stats['wasted_space']
        self.total_sequences_per_bin += stats['sequences_per_bin']
        self.total_bin_utilization += stats['bin_utilization']
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        num_sequences = len(sequence_lengths)
        num_bins = len(bins)
        total_sequence_length = sum(sequence_lengths)
        total_bin_capacity = bin_capacity * num_bins
        wasted_space = total_bin_capacity - total_sequence_length
        sequences_per_bin = num_sequences / num_bins if num_bins > 0 else 0
        bin_utilization = (total_sequence_length / total_bin_capacity) * \
            100 if total_bin_capacity > 0 else 0
        return {
            'num_sequences': num_sequences,
            'num_bins': num_bins,
            'total_sequence_length': total_sequence_length,
            'total_bin_capacity': total_bin_capacity,
            'wasted_space': wasted_space,
            'sequences_per_bin': sequences_per_bin,
            'bin_utilization': bin_utilization
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        avg_sequences_per_bin = self.total_sequences_per_bin / \
            self.total_bins if self.total_bins > 0 else 0
        avg_bin_utilization = self.total_bin_utilization / \
            self.total_bins if self.total_bins > 0 else 0
        return {
            'total_sequences': self.total_sequences,
            'total_bins': self.total_bins,
            'total_bin_capacity': self.total_bin_capacity,
            'total_packing_time': self.total_packing_time,
            'total_sequence_length': self.total_sequence_length,
            'total_wasted_space': self.total_wasted_space,
            'avg_sequences_per_bin': avg_sequences_per_bin,
            'avg_bin_utilization': avg_bin_utilization
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"Total Sequences: {stats['total_sequences']}")
        print(f"Total Bins: {stats['total_bins']}")
        print(f"Total Bin Capacity: {stats['total_bin_capacity']}")
        print(f"Total Packing Time: {stats['total_packing_time']:.2f} seconds")
        print(f"Total Sequence Length: {stats['total_sequence_length']}")
        print(f"Total Wasted Space: {stats['total_wasted_space']}")
        print(
            f"Average Sequences per Bin: {stats['avg_sequences_per_bin']:.2f}")
        print(f"Average Bin Utilization: {stats['avg_bin_utilization']:.2f}%")

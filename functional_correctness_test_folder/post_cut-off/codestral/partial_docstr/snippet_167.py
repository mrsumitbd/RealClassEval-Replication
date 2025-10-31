
from typing import List, Dict, Optional


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
        self.total_imbalance = 0
        self.total_packing_time = 0.0
        self.num_updates = 0

    def reset(self) -> None:
        self.total_sequences = 0
        self.total_bins = 0
        self.total_waste = 0
        self.total_imbalance = 0
        self.total_packing_time = 0.0
        self.num_updates = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_sequences += len(sequence_lengths)
        self.total_bins += len(bins)
        self.total_waste += stats['waste']
        self.total_imbalance += stats['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_updates += 1
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        bin_utilizations = [sum(sequence_lengths) /
                            bin_capacity for sequence_lengths in bins]
        avg_utilization = sum(bin_utilizations) / len(bin_utilizations)
        waste = sum(bin_capacity - sum(sequence_lengths)
                    for sequence_lengths in bins)
        imbalance = max(bin_utilizations) - min(bin_utilizations)
        return {
            'avg_utilization': avg_utilization,
            'waste': waste,
            'imbalance': imbalance
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        if self.num_updates == 0:
            return {
                'avg_utilization': 0.0,
                'waste': 0.0,
                'imbalance': 0.0,
                'avg_packing_time': 0.0
            }
        return {
            'avg_utilization': self.total_waste / (self.total_bins * self.num_updates),
            'waste': self.total_waste / self.num_updates,
            'imbalance': self.total_imbalance / self.num_updates,
            'avg_packing_time': self.total_packing_time / self.num_updates
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print(f"Average Utilization: {stats['avg_utilization']:.2f}")
        print(f"Waste: {stats['waste']:.2f}")
        print(f"Imbalance: {stats['imbalance']:.2f}")
        print(f"Average Packing Time: {stats['avg_packing_time']:.2f}")

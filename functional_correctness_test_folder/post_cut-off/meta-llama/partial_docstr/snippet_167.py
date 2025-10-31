
from typing import List, Dict, Optional


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        self.total_bins = 0
        self.total_bin_utilization = 0.0
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
        self.num_updates = 0

    def reset(self) -> None:
        self.total_bins = 0
        self.total_bin_utilization = 0.0
        self.total_waste = 0.0
        self.total_imbalance = 0.0
        self.total_packing_time = 0.0
        self.num_updates = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_bins += len(bins)
        self.total_bin_utilization += stats['bin_utilization']
        self.total_waste += stats['waste']
        self.total_imbalance += stats['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_updates += 1
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        total_sequence_length = sum(sequence_lengths)
        bin_utilization = sum(min(bin_capacity, sum(bin))
                              for bin in bins) / (len(bins) * bin_capacity)
        waste = 1 - (total_sequence_length / (len(bins) * bin_capacity))
        imbalance = max(len(bin) for bin in bins) - min(len(bin)
                                                        for bin in bins)
        return {
            'bin_utilization': bin_utilization,
            'waste': waste,
            'imbalance': imbalance
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        if self.num_updates == 0:
            return {
                'avg_bin_utilization': 0.0,
                'avg_waste': 0.0,
                'avg_imbalance': 0.0,
                'avg_packing_time': 0.0
            }
        return {
            'avg_bin_utilization': self.total_bin_utilization / self.num_updates,
            'avg_waste': self.total_waste / self.num_updates,
            'avg_imbalance': self.total_imbalance / self.num_updates,
            'avg_packing_time': self.total_packing_time / self.num_updates
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print("Aggregated Stats:")
        print(f"Average Bin Utilization: {stats['avg_bin_utilization']:.4f}")
        print(f"Average Waste: {stats['avg_waste']:.4f}")
        print(f"Average Imbalance: {stats['avg_imbalance']:.4f}")
        print(f"Average Packing Time: {stats['avg_packing_time']:.4f}")


from typing import List, Dict, Optional


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.total_sequences = 0
        self.total_bins = 0
        self.total_capacity = 0
        self.total_used = 0
        self.total_waste = 0
        self.total_imbalance = 0
        self.total_packing_time = 0.0
        self.num_updates = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.total_sequences += len(sequence_lengths)
        self.total_bins += len(bins)
        self.total_capacity += len(bins) * bin_capacity
        self.total_used += stats['total_used']
        self.total_waste += stats['total_waste']
        self.total_imbalance += stats['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_updates += 1
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        num_bins = len(bins)
        total_used = sum(sum(bin) for bin in bins)
        total_capacity = num_bins * bin_capacity
        total_waste = total_capacity - total_used
        utilizations = [sum(bin) / bin_capacity if bin_capacity >
                        0 else 0.0 for bin in bins]
        avg_utilization = sum(utilizations) / num_bins if num_bins > 0 else 0.0
        imbalance = max(utilizations) - \
            min(utilizations) if num_bins > 0 else 0.0
        stats = {
            'num_sequences': len(sequence_lengths),
            'num_bins': num_bins,
            'total_used': total_used,
            'total_capacity': total_capacity,
            'total_waste': total_waste,
            'avg_utilization': avg_utilization,
            'imbalance': imbalance
        }
        return stats

    def get_aggregated_stats(self) -> Dict[str, float]:
        if self.num_updates == 0:
            return {
                'avg_num_sequences': 0.0,
                'avg_num_bins': 0.0,
                'avg_total_used': 0.0,
                'avg_total_capacity': 0.0,
                'avg_total_waste': 0.0,
                'avg_utilization': 0.0,
                'avg_imbalance': 0.0,
                'avg_packing_time': 0.0
            }
        avg_num_sequences = self.total_sequences / self.num_updates
        avg_num_bins = self.total_bins / self.num_updates
        avg_total_used = self.total_used / self.num_updates
        avg_total_capacity = self.total_capacity / self.num_updates
        avg_total_waste = self.total_waste / self.num_updates
        avg_utilization = (
            self.total_used / self.total_capacity) if self.total_capacity > 0 else 0.0
        avg_imbalance = self.total_imbalance / self.num_updates
        avg_packing_time = self.total_packing_time / \
            self.num_updates if self.total_packing_time > 0 else 0.0
        return {
            'avg_num_sequences': avg_num_sequences,
            'avg_num_bins': avg_num_bins,
            'avg_total_used': avg_total_used,
            'avg_total_capacity': avg_total_capacity,
            'avg_total_waste': avg_total_waste,
            'avg_utilization': avg_utilization,
            'avg_imbalance': avg_imbalance,
            'avg_packing_time': avg_packing_time
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        for k, v in stats.items():
            print(f"  {k}: {v:.4f}")

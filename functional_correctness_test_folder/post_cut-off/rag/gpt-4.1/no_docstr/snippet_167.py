from typing import List, Dict, Optional


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.reset()

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.num_packs = 0
        self.total_bins = 0
        self.total_sequences = 0
        self.total_bin_utilization = 0.0
        self.total_bin_waste = 0.0
        self.total_bin_imbalance = 0.0
        self.total_packing_time = 0.0
        self.total_bins_used = 0
        self.total_full_bins = 0
        self.total_empty_bins = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        '''Update metrics with a new packing solution.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
            packing_time: Optional time taken to compute the packing solution
        Returns:
            Dictionary of metrics for this packing solution
        '''
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        self.num_packs += 1
        self.total_bins += stats['num_bins']
        self.total_sequences += stats['num_sequences']
        self.total_bin_utilization += stats['avg_bin_utilization']
        self.total_bin_waste += stats['avg_bin_waste']
        self.total_bin_imbalance += stats['bin_imbalance']
        self.total_bins_used += stats['num_bins']
        self.total_full_bins += stats['num_full_bins']
        self.total_empty_bins += stats['num_empty_bins']
        if packing_time is not None:
            self.total_packing_time += packing_time
        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        '''Calculate metrics for a packing solution without updating the tracker.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
        Returns:
            Dictionary of metrics for this packing solution
        '''
        num_bins = len(bins)
        num_sequences = len(sequence_lengths)
        bin_usages = []
        num_full_bins = 0
        num_empty_bins = 0
        for b in bins:
            usage = sum(sequence_lengths[i] for i in b)
            bin_usages.append(usage)
            if usage == 0:
                num_empty_bins += 1
            if usage == bin_capacity:
                num_full_bins += 1
        total_usage = sum(bin_usages)
        avg_bin_utilization = (total_usage / (num_bins * bin_capacity)
                               ) if num_bins > 0 and bin_capacity > 0 else 0.0
        avg_bin_waste = (sum(bin_capacity - u for u in bin_usages) /
                         num_bins) if num_bins > 0 else 0.0
        if bin_usages:
            max_usage = max(bin_usages)
            min_usage = min(bin_usages)
            bin_imbalance = max_usage - min_usage
        else:
            bin_imbalance = 0.0
        stats = {
            'num_bins': float(num_bins),
            'num_sequences': float(num_sequences),
            'avg_bin_utilization': avg_bin_utilization,
            'avg_bin_waste': avg_bin_waste,
            'bin_imbalance': float(bin_imbalance),
            'num_full_bins': float(num_full_bins),
            'num_empty_bins': float(num_empty_bins),
        }
        return stats

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.num_packs == 0:
            return {
                'num_packs': 0.0,
                'total_bins': 0.0,
                'total_sequences': 0.0,
                'avg_bin_utilization': 0.0,
                'avg_bin_waste': 0.0,
                'avg_bin_imbalance': 0.0,
                'avg_bins_per_pack': 0.0,
                'avg_full_bins_per_pack': 0.0,
                'avg_empty_bins_per_pack': 0.0,
                'avg_packing_time': 0.0,
            }
        return {
            'num_packs': float(self.num_packs),
            'total_bins': float(self.total_bins),
            'total_sequences': float(self.total_sequences),
            'avg_bin_utilization': self.total_bin_utilization / self.num_packs,
            'avg_bin_waste': self.total_bin_waste / self.num_packs,
            'avg_bin_imbalance': self.total_bin_imbalance / self.num_packs,
            'avg_bins_per_pack': self.total_bins_used / self.num_packs,
            'avg_full_bins_per_pack': self.total_full_bins / self.num_packs,
            'avg_empty_bins_per_pack': self.total_empty_bins / self.num_packs,
            'avg_packing_time': self.total_packing_time / self.num_packs if self.total_packing_time > 0 else 0.0,
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Packing Metrics (Aggregated):")
        print(f"  Number of packings: {stats['num_packs']:.0f}")
        print(f"  Total bins: {stats['total_bins']:.0f}")
        print(f"  Total sequences: {stats['total_sequences']:.0f}")
        print(f"  Avg. bin utilization: {stats['avg_bin_utilization']:.4f}")
        print(f"  Avg. bin waste: {stats['avg_bin_waste']:.4f}")
        print(f"  Avg. bin imbalance: {stats['avg_bin_imbalance']:.4f}")
        print(f"  Avg. bins per packing: {stats['avg_bins_per_pack']:.2f}")
        print(
            f"  Avg. full bins per packing: {stats['avg_full_bins_per_pack']:.2f}")
        print(
            f"  Avg. empty bins per packing: {stats['avg_empty_bins_per_pack']:.2f}")
        print(f"  Avg. packing time: {stats['avg_packing_time']:.4f} seconds")

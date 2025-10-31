
class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        '''Initialize the metrics tracker.'''
        self.total_sequences = 0
        self.total_bins = 0
        self.total_waste = 0
        self.total_utilization = 0
        self.total_imbalance = 0
        self.total_packing_time = 0
        self.num_packing_operations = 0

    def reset(self) -> None:
        '''Reset all metrics.'''
        self.total_sequences = 0
        self.total_bins = 0
        self.total_waste = 0
        self.total_utilization = 0
        self.total_imbalance = 0
        self.total_packing_time = 0
        self.num_packing_operations = 0

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
        metrics = self.calculate_stats_only(
            sequence_lengths, bins, bin_capacity)

        self.total_sequences += len(sequence_lengths)
        self.total_bins += len(bins)
        self.total_waste += metrics['waste']
        self.total_utilization += metrics['utilization']
        self.total_imbalance += metrics['imbalance']
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_packing_operations += 1

        return metrics

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        '''Calculate metrics for a packing solution without updating the tracker.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
        Returns:
            Dictionary of metrics for this packing solution
        '''
        bin_utilizations = []
        bin_wastes = []

        for bin_indices in bins:
            bin_sum = sum(sequence_lengths[i] for i in bin_indices)
            bin_utilization = bin_sum / bin_capacity
            bin_waste = bin_capacity - bin_sum

            bin_utilizations.append(bin_utilization)
            bin_wastes.append(bin_waste)

        avg_utilization = sum(bin_utilizations) / \
            len(bin_utilizations) if bin_utilizations else 0
        avg_waste = sum(bin_wastes) / len(bin_wastes) if bin_wastes else 0
        imbalance = max(bin_utilizations) - \
            min(bin_utilizations) if bin_utilizations else 0

        return {
            'utilization': avg_utilization,
            'waste': avg_waste,
            'imbalance': imbalance,
            'num_bins': len(bins),
            'num_sequences': len(sequence_lengths)
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        if self.num_packing_operations == 0:
            return {
                'avg_utilization': 0,
                'avg_waste': 0,
                'avg_imbalance': 0,
                'avg_bins_per_operation': 0,
                'avg_sequences_per_operation': 0,
                'avg_packing_time': 0
            }

        return {
            'avg_utilization': self.total_utilization / self.num_packing_operations,
            'avg_waste': self.total_waste / self.num_packing_operations,
            'avg_imbalance': self.total_imbalance / self.num_packing_operations,
            'avg_bins_per_operation': self.total_bins / self.num_packing_operations,
            'avg_sequences_per_operation': self.total_sequences / self.num_packing_operations,
            'avg_packing_time': self.total_packing_time / self.num_packing_operations
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Average Utilization: {stats['avg_utilization']:.2%}")
        print(f"  Average Waste: {stats['avg_waste']:.2f}")
        print(f"  Average Imbalance: {stats['avg_imbalance']:.2%}")
        print(
            f"  Average Bins per Operation: {stats['avg_bins_per_operation']:.2f}")
        print(
            f"  Average Sequences per Operation: {stats['avg_sequences_per_operation']:.2f}")
        print(
            f"  Average Packing Time: {stats['avg_packing_time']:.4f} seconds")

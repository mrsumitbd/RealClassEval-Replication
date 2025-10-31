from typing import Dict, List, Optional
import math


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
        # Run counters
        self._runs = 0
        self._timed_runs = 0

        # Aggregated totals (sums)
        self._total_sequences = 0
        self._total_tokens = 0.0
        self._total_bins = 0
        self._total_capacity = 0.0
        self._total_assigned_tokens = 0.0
        self._total_unique_packed_tokens = 0.0
        self._total_packed_sequences = 0
        self._total_waste = 0.0
        self._total_empty_bins = 0
        self._total_overflow = 0.0
        self._total_overflow_bins = 0
        self._total_avg_items_per_bin = 0.0  # sum of per-run averages
        self._total_avg_bin_utilization = 0.0  # sum of per-run averages
        self._total_imbalance_cv = 0.0  # sum of per-run CVs
        self._total_fill_ratio = 0.0  # sum of per-run fill ratios
        self._total_waste_ratio = 0.0  # sum of per-run waste ratios
        self._total_time = 0.0

        # Aggregated extrema across runs
        self._min_fill_ratio = float('inf')
        self._max_fill_ratio = float('-inf')
        self._min_imbalance_cv = float('inf')
        self._max_imbalance_cv = float('-inf')
        self._min_waste_ratio = float('inf')
        self._max_waste_ratio = float('-inf')

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
        # Add timing-based metrics
        if packing_time is not None and packing_time > 0:
            stats['packing_time'] = float(packing_time)
            stats['sequences_per_s'] = float(
                len(sequence_lengths)) / float(packing_time)
            stats['tokens_per_s'] = float(
                stats['assigned_tokens']) / float(packing_time)
        else:
            stats['packing_time'] = float(
                packing_time) if packing_time is not None else 0.0
            stats['sequences_per_s'] = 0.0
            stats['tokens_per_s'] = 0.0

        # Update aggregates
        self._runs += 1
        if packing_time is not None:
            self._timed_runs += 1
            self._total_time += float(packing_time)

        self._total_sequences += int(stats['total_sequences'])
        self._total_tokens += float(stats['total_tokens'])
        self._total_bins += int(stats['num_bins'])
        self._total_capacity += float(stats['total_capacity'])
        self._total_assigned_tokens += float(stats['assigned_tokens'])
        self._total_unique_packed_tokens += float(
            stats['unique_packed_tokens'])
        self._total_packed_sequences += int(stats['packed_sequences'])
        self._total_waste += float(stats['waste'])
        self._total_empty_bins += int(stats['empty_bins'])
        self._total_overflow += float(stats['overflow_total'])
        self._total_overflow_bins += int(stats['overflow_bins'])
        self._total_avg_items_per_bin += float(stats['avg_items_per_bin'])
        self._total_avg_bin_utilization += float(stats['avg_bin_utilization'])
        self._total_imbalance_cv += float(stats['imbalance_cv'])
        self._total_fill_ratio += float(stats['fill_ratio'])
        self._total_waste_ratio += float(stats['waste_ratio'])

        self._min_fill_ratio = min(
            self._min_fill_ratio, float(stats['fill_ratio']))
        self._max_fill_ratio = max(
            self._max_fill_ratio, float(stats['fill_ratio']))
        self._min_imbalance_cv = min(
            self._min_imbalance_cv, float(stats['imbalance_cv']))
        self._max_imbalance_cv = max(
            self._max_imbalance_cv, float(stats['imbalance_cv']))
        self._min_waste_ratio = min(
            self._min_waste_ratio, float(stats['waste_ratio']))
        self._max_waste_ratio = max(
            self._max_waste_ratio, float(stats['waste_ratio']))

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
        n_bins = len(bins)
        total_sequences = len(sequence_lengths)
        total_tokens = float(sum(max(0, int(x)) for x in sequence_lengths))

        cap = float(max(0, int(bin_capacity)))
        total_capacity = cap * float(n_bins)

        # Prepare per-bin loads and counts
        valid_len = len(sequence_lengths)
        bin_loads: List[float] = []
        bin_item_counts: List[int] = []
        assigned_tokens = 0.0
        overflow_total = 0.0
        overflow_bins = 0
        empty_bins = 0
        invalid_indices = 0

        # Track unique packed indices
        unique_indices = set()

        for b in bins:
            load = 0.0
            item_count = 0
            for idx in b:
                if isinstance(idx, int) and 0 <= idx < valid_len:
                    length = float(max(0, int(sequence_lengths[idx])))
                    load += length
                    item_count += 1
                    unique_indices.add(idx)
                else:
                    invalid_indices += 1
            bin_loads.append(load)
            bin_item_counts.append(item_count)
            assigned_tokens += load
            if cap > 0 and load == 0:
                empty_bins += 1
            if cap > 0 and load > cap:
                overflow = load - cap
                overflow_total += overflow
                overflow_bins += 1

        # Utilization metrics
        if n_bins > 0 and cap > 0:
            per_bin_util = [load / cap for load in bin_loads]
            avg_bin_utilization = float(sum(per_bin_util) / n_bins)
            min_bin_utilization = float(
                min(per_bin_util)) if per_bin_util else 0.0
            max_bin_utilization = float(
                max(per_bin_util)) if per_bin_util else 0.0

            # Imbalance as coefficient of variation (std / mean)
            mean_u = avg_bin_utilization
            if n_bins > 1 and mean_u != 0.0:
                var = sum((u - mean_u) ** 2 for u in per_bin_util) / n_bins
                std = math.sqrt(var)
                imbalance_cv = float(std / abs(mean_u))
                stdev_bin_utilization = float(std)
            else:
                imbalance_cv = 0.0
                stdev_bin_utilization = 0.0
        else:
            avg_bin_utilization = 0.0
            min_bin_utilization = 0.0
            max_bin_utilization = 0.0
            imbalance_cv = 0.0
            stdev_bin_utilization = 0.0

        # Global utilization and waste
        used = float(assigned_tokens)
        if total_capacity > 0.0:
            fill_ratio = float(used / total_capacity)
            waste = float(max(0.0, total_capacity - used))
            waste_ratio = float(waste / total_capacity)
        else:
            fill_ratio = 0.0
            waste = 0.0
            waste_ratio = 0.0

        avg_items_per_bin = float(
            sum(bin_item_counts) / n_bins) if n_bins > 0 else 0.0

        packed_sequences = len(unique_indices)
        unpacked_sequences = max(0, total_sequences - packed_sequences)
        packed_ratio = float(packed_sequences /
                             total_sequences) if total_sequences > 0 else 0.0
        unique_packed_tokens = float(
            sum(float(max(0, int(sequence_lengths[i]))) for i in unique_indices))

        return {
            'num_bins': float(n_bins),
            'bin_capacity': float(cap),
            'total_capacity': float(total_capacity),
            'total_sequences': float(total_sequences),
            'total_tokens': float(total_tokens),
            'assigned_tokens': float(assigned_tokens),
            'unique_packed_tokens': float(unique_packed_tokens),
            'packed_sequences': float(packed_sequences),
            'unpacked_sequences': float(unpacked_sequences),
            'packed_ratio': float(packed_ratio),
            'fill_ratio': float(fill_ratio),
            'waste': float(waste),
            'waste_ratio': float(waste_ratio),
            'avg_bin_utilization': float(avg_bin_utilization),
            'min_bin_utilization': float(min_bin_utilization),
            'max_bin_utilization': float(max_bin_utilization),
            'stdev_bin_utilization': float(stdev_bin_utilization),
            'imbalance_cv': float(imbalance_cv),
            'empty_bins': float(empty_bins),
            'overflow_total': float(overflow_total),
            'overflow_bins': float(overflow_bins),
            'avg_items_per_bin': float(avg_items_per_bin),
            'invalid_indices': float(invalid_indices),
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        '''Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        '''
        runs = self._runs
        timed_runs = self._timed_runs

        avg_bins_per_run = float(self._total_bins / runs) if runs > 0 else 0.0
        avg_fill_ratio = float(self._total_fill_ratio /
                               runs) if runs > 0 else 0.0
        avg_waste_ratio = float(
            self._total_waste_ratio / runs) if runs > 0 else 0.0
        avg_imbalance_cv = float(
            self._total_imbalance_cv / runs) if runs > 0 else 0.0
        avg_items_per_bin = float(
            self._total_avg_items_per_bin / runs) if runs > 0 else 0.0
        avg_bin_utilization = float(
            self._total_avg_bin_utilization / runs) if runs > 0 else 0.0

        overall_fill_ratio = float(
            (self._total_assigned_tokens / self._total_capacity)
        ) if self._total_capacity > 0 else 0.0
        overall_waste_ratio = float(
            (self._total_waste / self._total_capacity)
        ) if self._total_capacity > 0 else 0.0

        avg_time_per_run = float(
            self._total_time / timed_runs) if timed_runs > 0 else 0.0
        sequences_per_s = float(
            self._total_sequences / self._total_time) if self._total_time > 0 else 0.0
        tokens_per_s = float(self._total_assigned_tokens /
                             self._total_time) if self._total_time > 0 else 0.0

        min_fill_ratio = 0.0 if runs == 0 else float(self._min_fill_ratio)
        max_fill_ratio = 0.0 if runs == 0 else float(self._max_fill_ratio)
        min_imbalance_cv = 0.0 if runs == 0 else float(self._min_imbalance_cv)
        max_imbalance_cv = 0.0 if runs == 0 else float(self._max_imbalance_cv)
        min_waste_ratio = 0.0 if runs == 0 else float(self._min_waste_ratio)
        max_waste_ratio = 0.0 if runs == 0 else float(self._max_waste_ratio)

        return {
            'runs': float(runs),
            'timed_runs': float(timed_runs),
            'total_sequences': float(self._total_sequences),
            'total_packed_sequences': float(self._total_packed_sequences),
            'total_tokens': float(self._total_tokens),
            'total_assigned_tokens': float(self._total_assigned_tokens),
            'total_unique_packed_tokens': float(self._total_unique_packed_tokens),
            'total_bins': float(self._total_bins),
            'total_capacity': float(self._total_capacity),
            'total_waste': float(self._total_waste),
            'total_empty_bins': float(self._total_empty_bins),
            'total_overflow': float(self._total_overflow),
            'total_overflow_bins': float(self._total_overflow_bins),

            'avg_bins_per_run': float(avg_bins_per_run),
            'avg_fill_ratio': float(avg_fill_ratio),
            'avg_waste_ratio': float(avg_waste_ratio),
            'avg_imbalance_cv': float(avg_imbalance_cv),
            'avg_items_per_bin': float(avg_items_per_bin),
            'avg_bin_utilization': float(avg_bin_utilization),

            'overall_fill_ratio': float(overall_fill_ratio),
            'overall_waste_ratio': float(overall_waste_ratio),

            'min_fill_ratio': float(min_fill_ratio),
            'max_fill_ratio': float(max_fill_ratio),
            'min_imbalance_cv': float(min_imbalance_cv),
            'max_imbalance_cv': float(max_imbalance_cv),
            'min_waste_ratio': float(min_waste_ratio),
            'max_waste_ratio': float(max_waste_ratio),

            'total_time': float(self._total_time),
            'avg_time_per_run': float(avg_time_per_run),
            'sequences_per_s': float(sequences_per_s),
            'tokens_per_s': float(tokens_per_s),
        }

    def print_aggregated_stats(self) -> None:
        '''Print the aggregated metrics in a formatted way.'''
        stats = self.get_aggregated_stats()
        print('Packing Metrics (Aggregated)')
        print('---------------------------')
        print(
            f"Runs: {int(stats['runs'])} (timed: {int(stats['timed_runs'])})")
        print(
            f"Total sequences: {int(stats['total_sequences'])} | Packed: {int(stats['total_packed_sequences'])}")
        print(
            f"Total tokens: {stats['total_tokens']:.0f} | Assigned tokens: {stats['total_assigned_tokens']:.0f}")
        print(
            f"Total bins: {int(stats['total_bins'])} | Total capacity: {stats['total_capacity']:.0f}")
        print(
            f"Total waste: {stats['total_waste']:.0f} | Empty bins: {int(stats['total_empty_bins'])}")
        print(
            f"Overflow tokens: {stats['total_overflow']:.0f} | Overflow bins: {int(stats['total_overflow_bins'])}")
        print()
        print(
            f"Overall fill ratio: {stats['overall_fill_ratio']:.4f} | Overall waste ratio: {stats['overall_waste_ratio']:.4f}")
        print(
            f"Average fill ratio: {stats['avg_fill_ratio']:.4f} (min: {stats['min_fill_ratio']:.4f}, max: {stats['max_fill_ratio']:.4f})")
        print(f"Average bin utilization: {stats['avg_bin_utilization']:.4f}")
        print(
            f"Imbalance (CV): avg {stats['avg_imbalance_cv']:.4f} (min: {stats['min_imbalance_cv']:.4f}, max: {stats['max_imbalance_cv']:.4f})")
        print(
            f"Avg items/bin: {stats['avg_items_per_bin']:.4f} | Avg bins/run: {stats['avg_bins_per_run']:.4f}")
        print()
        print(
            f"Total time (s): {stats['total_time']:.3f} | Avg time/run (s): {stats['avg_time_per_run']:.3f}")
        print(
            f"Throughput: {stats['sequences_per_s']:.3f} seq/s | {stats['tokens_per_s']:.3f} tokens/s")

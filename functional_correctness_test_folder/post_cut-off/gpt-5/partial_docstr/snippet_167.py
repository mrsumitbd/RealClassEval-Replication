from typing import List, Optional, Dict
import math
import statistics


class PackingMetrics:
    '''Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    '''

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._runs = 0
        self._total_sequences = 0
        self._total_bins = 0
        self._total_capacity = 0
        self._total_used_capacity = 0
        self._sum_utilization = 0.0
        self._sum_waste = 0.0
        self._sum_avg_bin_fill = 0.0
        self._sum_stdev_bin_fill = 0.0
        self._sum_imbalance = 0.0
        self._total_overflow_amount = 0
        self._total_empty_bins = 0
        self._overfilled_runs = 0
        self._perfect_packing_runs = 0
        self._valid_runs = 0  # runs without any overflow
        self._total_packing_time = 0.0
        self._packing_time_samples = 0

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)

        self._runs += 1
        self._total_sequences += int(stats["num_sequences"])
        self._total_bins += int(stats["num_bins"])
        self._total_capacity += int(stats["total_capacity"])
        self._total_used_capacity += int(stats["used_capacity"])

        self._sum_utilization += stats["utilization"]
        self._sum_waste += stats["waste"]
        self._sum_avg_bin_fill += stats["avg_bin_fill"]
        self._sum_stdev_bin_fill += stats["stdev_bin_fill"]
        self._sum_imbalance += stats["imbalance"]
        self._total_overflow_amount += int(stats["total_overflow"])
        self._total_empty_bins += int(stats["empty_bins"])

        if stats["has_overflow"] > 0.0:
            self._overfilled_runs += 1
        else:
            self._valid_runs += 1

        if stats["perfect_packing"] > 0.0:
            self._perfect_packing_runs += 1

        if packing_time is not None:
            self._total_packing_time += float(packing_time)
            self._packing_time_samples += 1
            stats["packing_time"] = float(packing_time)
        else:
            stats["packing_time"] = float("nan")

        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        num_sequences = len(
            sequence_lengths) if sequence_lengths is not None else 0
        num_bins = len(bins) if bins is not None else 0
        cap = int(bin_capacity) if bin_capacity is not None else 0

        if bins is None:
            bins = []
        bin_loads = [sum(b) for b in bins]
        used_capacity = sum(bin_loads)
        seq_sum = sum(
            sequence_lengths) if sequence_lengths is not None else used_capacity

        # Prefer bin loads as ground truth for used capacity if provided
        used = used_capacity
        total_capacity = num_bins * cap

        utilization = (used / total_capacity) if total_capacity > 0 else 0.0
        utilization = min(max(utilization, 0.0), 1.0) if cap > 0 and all(
            x <= cap for x in bin_loads) else (used / total_capacity if total_capacity > 0 else 0.0)
        waste = 1.0 - utilization if total_capacity > 0 else 0.0

        # Per-bin fill ratios (clipped to non-negative; not clipped on upper to reflect overflow in stats)
        fill_ratios = [(load / cap) if cap > 0 else 0.0 for load in bin_loads]
        avg_bin_fill = (sum(fill_ratios) / num_bins) if num_bins > 0 else 0.0
        if num_bins >= 2:
            try:
                stdev_bin_fill = float(statistics.pstdev(fill_ratios))
            except statistics.StatisticsError:
                stdev_bin_fill = 0.0
        else:
            stdev_bin_fill = 0.0

        max_load = max(bin_loads) if num_bins > 0 else 0
        min_load = min(bin_loads) if num_bins > 0 else 0
        imbalance = ((max_load - min_load) /
                     cap) if cap > 0 and num_bins > 0 else 0.0

        empty_bins = sum(1 for load in bin_loads if load == 0)
        overflow_amounts = [
            max(0, load - cap) for load in bin_loads] if cap > 0 else [0 for _ in bin_loads]
        total_overflow = sum(overflow_amounts)
        has_overflow = 1.0 if total_overflow > 0 else 0.0

        perfect_packing = 1.0 if (
            has_overflow == 0.0 and total_capacity > 0 and used == total_capacity) else 0.0

        mismatch_abs = abs(seq_sum - used)
        mismatch_ratio = (
            mismatch_abs / used) if used > 0 else (0.0 if mismatch_abs == 0 else float("inf"))

        return {
            "num_sequences": float(num_sequences),
            "num_bins": float(num_bins),
            "bin_capacity": float(cap),
            "total_capacity": float(total_capacity),
            "used_capacity": float(used),
            "utilization": float(utilization),
            "waste": float(waste),
            "avg_bin_fill": float(avg_bin_fill),
            "stdev_bin_fill": float(stdev_bin_fill),
            "max_bin_fill": float((max_load / cap) if cap > 0 else 0.0),
            "min_bin_fill": float((min_load / cap) if cap > 0 else 0.0),
            "imbalance": float(imbalance),
            "empty_bins": float(empty_bins),
            "total_overflow": float(total_overflow),
            "has_overflow": float(has_overflow),
            "perfect_packing": float(perfect_packing),
            "seq_bin_sum_mismatch": float(mismatch_abs),
            "seq_bin_sum_mismatch_ratio": float(mismatch_ratio),
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        runs = self._runs if self._runs > 0 else 1  # avoid div by zero for averages

        return {
            "runs": float(self._runs),
            "total_sequences": float(self._total_sequences),
            "total_bins": float(self._total_bins),
            "total_capacity": float(self._total_capacity),
            "total_used_capacity": float(self._total_used_capacity),

            "avg_utilization": float(self._sum_utilization / runs),
            "avg_waste": float(self._sum_waste / runs),
            "avg_bin_fill": float(self._sum_avg_bin_fill / runs),
            "avg_stdev_bin_fill": float(self._sum_stdev_bin_fill / runs),
            "avg_imbalance": float(self._sum_imbalance / runs),

            "total_overflow": float(self._total_overflow_amount),
            "total_empty_bins": float(self._total_empty_bins),

            "overfilled_runs": float(self._overfilled_runs),
            "valid_runs": float(self._valid_runs),
            "perfect_packing_runs": float(self._perfect_packing_runs),

            "total_packing_time": float(self._total_packing_time),
            "avg_packing_time": float((self._total_packing_time / self._packing_time_samples) if self._packing_time_samples > 0 else float("nan")),
        }

    def print_aggregated_stats(self) -> None:
        stats = self.get_aggregated_stats()
        for k in sorted(stats.keys()):
            print(f"{k}: {stats[k]}")

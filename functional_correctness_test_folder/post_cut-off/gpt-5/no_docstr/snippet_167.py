from typing import List, Optional, Dict, Tuple, Set


class PackingMetrics:
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._updates = 0

        self._cum_sequences = 0
        self._cum_bins = 0

        self._cum_sum_lengths = 0
        self._cum_total_capacity = 0
        self._cum_used_capacity = 0
        self._cum_waste = 0

        self._cum_empty_bins = 0
        self._cum_overflow_bins = 0

        self._sum_efficiency_per_update = 0.0
        self._sum_avg_util_per_update = 0.0

        self._cum_packing_time = 0.0
        self._num_times = 0

    def _bin_used_capacity(self, bin_items: List[int], sequence_lengths: List[int]) -> Tuple[int, Optional[Set[int]]]:
        if all((isinstance(x, int) and 0 <= x < len(sequence_lengths)) for x in bin_items):
            used = sum(sequence_lengths[x] for x in bin_items)
            return used, set(bin_items)
        else:
            used = sum(int(x) for x in bin_items) if bin_items else 0
            return used, None

    def _compute_stats(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        num_sequences = len(sequence_lengths)
        sum_sequence_lengths = int(sum(sequence_lengths))
        num_bins = len(bins)
        total_bin_capacity = int(num_bins * bin_capacity)

        used_per_bin: List[int] = []
        packed_indices: Set[int] = set()
        any_index_mode = False

        for b in bins:
            used, indices = self._bin_used_capacity(b, sequence_lengths)
            used_per_bin.append(int(used))
            if indices is not None:
                any_index_mode = True
                packed_indices.update(indices)

        total_used_capacity = int(sum(used_per_bin))
        waste = int(max(0, total_bin_capacity - total_used_capacity))

        overflow_bins = sum(1 for u in used_per_bin if u > bin_capacity)
        empty_bins = sum(1 for u in used_per_bin if u == 0)

        if total_bin_capacity > 0:
            packing_efficiency = total_used_capacity / total_bin_capacity
        else:
            packing_efficiency = 0.0

        if num_bins > 0 and bin_capacity > 0:
            utilizations = [min(u / bin_capacity, 1.0)
                            if bin_capacity > 0 else 0.0 for u in used_per_bin]
            avg_bin_utilization = sum(utilizations) / num_bins
            min_bin_utilization = min(utilizations)
            max_bin_utilization = max(utilizations)
        else:
            avg_bin_utilization = 0.0
            min_bin_utilization = 0.0
            max_bin_utilization = 0.0

        fit_ok = 1.0 if overflow_bins == 0 else 0.0
        sequences_packed = float(
            len(packed_indices)) if any_index_mode else float("nan")

        stats: Dict[str, float] = {
            "num_sequences": float(num_sequences),
            "num_bins": float(num_bins),
            "sum_sequence_lengths": float(sum_sequence_lengths),
            "bin_capacity": float(bin_capacity),
            "total_bin_capacity": float(total_bin_capacity),
            "total_used_capacity": float(total_used_capacity),
            "waste": float(waste),
            "packing_efficiency": float(packing_efficiency),
            "avg_bin_utilization": float(avg_bin_utilization),
            "min_bin_utilization": float(min_bin_utilization),
            "max_bin_utilization": float(max_bin_utilization),
            "empty_bins": float(empty_bins),
            "overflow_bins": float(overflow_bins),
            "fit_ok": float(fit_ok),
            "sequences_packed": float(sequences_packed) if sequences_packed == sequences_packed else float("nan"),
        }
        if packing_time is not None:
            stats["packing_time"] = float(packing_time)
        return stats

    def update(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int, packing_time: Optional[float] = None) -> Dict[str, float]:
        stats = self._compute_stats(
            sequence_lengths, bins, bin_capacity, packing_time)

        self._updates += 1

        self._cum_sequences += int(stats["num_sequences"])
        self._cum_bins += int(stats["num_bins"])

        self._cum_sum_lengths += int(stats["sum_sequence_lengths"])
        self._cum_total_capacity += int(stats["total_bin_capacity"])
        self._cum_used_capacity += int(stats["total_used_capacity"])
        self._cum_waste += int(stats["waste"])

        self._cum_empty_bins += int(stats["empty_bins"])
        self._cum_overflow_bins += int(stats["overflow_bins"])

        self._sum_efficiency_per_update += float(stats["packing_efficiency"])
        self._sum_avg_util_per_update += float(stats["avg_bin_utilization"])

        if packing_time is not None:
            self._cum_packing_time += float(packing_time)
            self._num_times += 1

        return stats

    def calculate_stats_only(self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int) -> Dict[str, float]:
        return self._compute_stats(sequence_lengths, bins, bin_capacity, None)

    def get_aggregated_stats(self) -> Dict[str, float]:
        updates = self._updates

        mean_packing_efficiency = (
            self._sum_efficiency_per_update / updates) if updates > 0 else 0.0
        mean_avg_bin_utilization = (
            self._sum_avg_util_per_update / updates) if updates > 0 else 0.0

        overall_efficiency = (
            self._cum_used_capacity / self._cum_total_capacity) if self._cum_total_capacity > 0 else 0.0
        overall_avg_bin_utilization = overall_efficiency

        mean_packing_time = (
            self._cum_packing_time / self._num_times) if self._num_times > 0 else float("nan")

        return {
            "updates": float(updates),
            "total_sequences": float(self._cum_sequences),
            "total_bins": float(self._cum_bins),
            "total_sum_sequence_lengths": float(self._cum_sum_lengths),
            "total_bin_capacity": float(self._cum_total_capacity),
            "total_used_capacity": float(self._cum_used_capacity),
            "total_waste": float(self._cum_waste),
            "total_empty_bins": float(self._cum_empty_bins),
            "total_overflow_bins": float(self._cum_overflow_bins),
            "mean_packing_efficiency": float(mean_packing_efficiency),
            "overall_efficiency": float(overall_efficiency),
            "mean_avg_bin_utilization": float(mean_avg_bin_utilization),
            "overall_avg_bin_utilization": float(overall_avg_bin_utilization),
            "total_packing_time": float(self._cum_packing_time),
            "mean_packing_time": float(mean_packing_time),
        }

    def print_aggregated_stats(self) -> None:
        agg = self.get_aggregated_stats()
        keys = [
            "updates",
            "total_sequences",
            "total_bins",
            "total_sum_sequence_lengths",
            "total_bin_capacity",
            "total_used_capacity",
            "total_waste",
            "total_empty_bins",
            "total_overflow_bins",
            "mean_packing_efficiency",
            "overall_efficiency",
            "mean_avg_bin_utilization",
            "overall_avg_bin_utilization",
            "total_packing_time",
            "mean_packing_time",
        ]
        for k in keys:
            v = agg.get(k)
            print(f"{k}: {v}")

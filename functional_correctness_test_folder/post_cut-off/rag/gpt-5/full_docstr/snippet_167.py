from typing import Dict, List, Optional
import math


class PackingMetrics:
    """Class for tracking and computing metrics for sequence packing algorithms.
    This class provides methods to calculate various metrics that evaluate the
    efficiency and effectiveness of sequence packing algorithms, such as bin
    utilization, waste, and imbalance.
    """

    def __init__(self):
        """Initialize the metrics tracker."""
        self.reset()

    def reset(self) -> None:
        """Reset all metrics."""
        self._ops = 0
        self._total_sequences = 0
        self._total_length = 0

        self._total_bins = 0
        self._total_capacity = 0

        # sum of raw lengths placed in bins (can exceed capacity)
        self._total_assigned_length = 0
        # sum of min(fill, capacity) across bins
        self._total_effective_used_length = 0
        self._total_waste = 0  # capacity not used
        self._total_overflow = 0  # amount exceeding capacity

        self._sum_std_fill_ratio = 0.0
        self._num_full_bins = 0

        # sum of per-op utilizations for unweighted avg
        self._sum_utilization_unweighted = 0.0
        self._best_utilization = None
        self._worst_utilization = None

        self._total_packing_time = 0.0
        self._num_packing_time = 0

    def update(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int,
        packing_time: Optional[float] = None,
    ) -> Dict[str, float]:
        """Update metrics with a new packing solution.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
            packing_time: Optional time taken to compute the packing solution
        Returns:
            Dictionary of metrics for this packing solution
        """
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)

        # Update aggregated counters
        self._ops += 1
        self._total_sequences += int(stats["num_sequences"])
        self._total_length += float(stats["total_length"])
        self._total_bins += int(stats["num_bins"])
        self._total_capacity += float(stats["total_capacity"])

        self._total_assigned_length += float(stats["assigned_length"])
        self._total_effective_used_length += float(
            stats["effective_used_length"])
        self._total_waste += float(stats["waste"])
        self._total_overflow += float(stats["overflow"])

        self._sum_std_fill_ratio += float(stats["std_fill_ratio"])
        self._num_full_bins += int(stats["num_full_bins"])

        util = float(stats["utilization"])
        self._sum_utilization_unweighted += util
        if self._best_utilization is None or util > self._best_utilization:
            self._best_utilization = util
        if self._worst_utilization is None or util < self._worst_utilization:
            self._worst_utilization = util

        if packing_time is not None:
            self._total_packing_time += float(packing_time)
            self._num_packing_time += 1
            stats["packing_time"] = float(packing_time)

        return stats

    def calculate_stats_only(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int,
    ) -> Dict[str, float]:
        """Calculate metrics for a packing solution without updating the tracker.
        Args:
            sequence_lengths: List of sequence lengths
            bins: List of bins, where each bin is a list of indices
            bin_capacity: Maximum capacity of each bin
        Returns:
            Dictionary of metrics for this packing solution
        """
        n_seq = len(sequence_lengths)
        num_bins = len(bins)
        total_length = float(sum(max(0, int(x)) for x in sequence_lengths))
        total_capacity = float(num_bins * max(0, int(bin_capacity)))
        cap = max(0, int(bin_capacity))

        # Compute per-bin raw fill and clamped fill
        per_bin_raw_fill: List[float] = []
        per_bin_used: List[float] = []
        seen = [False] * n_seq

        for b in bins:
            raw = 0
            for idx in b:
                if isinstance(idx, int) and 0 <= idx < n_seq:
                    raw += max(0, int(sequence_lengths[idx]))
                    seen[idx] = True
            per_bin_raw_fill.append(float(raw))
            used = float(min(raw, cap)) if cap > 0 else 0.0
            per_bin_used.append(used)

        assigned_length = float(sum(per_bin_raw_fill))
        effective_used_length = float(sum(per_bin_used))
        overflow = float(sum(max(0.0, rf - cap)
                         for rf in per_bin_raw_fill)) if cap > 0 else assigned_length
        waste = float(max(0.0, total_capacity - effective_used_length))

        # Fill ratios based on used (clamped to capacity)
        fill_ratios: List[float] = []
        if cap > 0 and num_bins > 0:
            fill_ratios = [u / cap for u in per_bin_used]
        elif num_bins > 0:
            fill_ratios = [0.0] * num_bins

        avg_fill_ratio = float(
            sum(fill_ratios) / num_bins) if num_bins > 0 else 0.0
        if num_bins > 1:
            mean = avg_fill_ratio
            var = sum((x - mean) ** 2 for x in fill_ratios) / num_bins
            std_fill_ratio = float(math.sqrt(var))
        else:
            std_fill_ratio = 0.0

        min_fill_ratio = float(min(fill_ratios)) if fill_ratios else 0.0
        max_fill_ratio = float(max(fill_ratios)) if fill_ratios else 0.0
        num_full_bins = int(
            sum(1 for rf in per_bin_raw_fill if rf >= cap)) if cap > 0 else 0
        frac_full_bins = float(
            num_full_bins / num_bins) if num_bins > 0 else 0.0

        utilized = float(effective_used_length /
                         total_capacity) if total_capacity > 0 else 0.0
        waste_ratio = float(
            waste / total_capacity) if total_capacity > 0 else 0.0
        overflow_ratio_capacity = float(
            overflow / total_capacity) if total_capacity > 0 else 0.0

        uncovered_length = float(
            sum(max(0, int(sequence_lengths[i]))
                for i in range(n_seq) if not seen[i])
        )
        coverage_ratio = float(
            assigned_length / total_length) if total_length > 0 else 1.0

        stats: Dict[str, float] = {
            "num_sequences": float(n_seq),
            "num_bins": float(num_bins),
            "bin_capacity": float(cap),
            "total_length": total_length,
            "assigned_length": assigned_length,
            "unpacked_length": uncovered_length,
            "total_capacity": total_capacity,
            "effective_used_length": effective_used_length,
            "utilization": utilized,
            "waste": waste,
            "waste_ratio": waste_ratio,
            "overflow": overflow,
            "overflow_ratio_capacity": overflow_ratio_capacity,
            "avg_fill_ratio": avg_fill_ratio,
            "std_fill_ratio": std_fill_ratio,
            "min_fill_ratio": min_fill_ratio,
            "max_fill_ratio": max_fill_ratio,
            "num_full_bins": float(num_full_bins),
            "frac_full_bins": frac_full_bins,
            "coverage_ratio": coverage_ratio,
        }
        return stats

    def get_aggregated_stats(self) -> Dict[str, float]:
        """Get aggregated metrics across all packing operations.
        Returns:
            Dictionary of aggregated metrics
        """
        ops = self._ops
        total_bins = self._total_bins
        total_capacity = self._total_capacity

        overall_utilization = (
            float(self._total_effective_used_length /
                  total_capacity) if total_capacity > 0 else 0.0
        )
        overall_waste_ratio = (
            float(self._total_waste / total_capacity) if total_capacity > 0 else 0.0
        )
        avg_std_fill_ratio = float(
            self._sum_std_fill_ratio / ops) if ops > 0 else 0.0
        avg_bins_per_op = float(total_bins / ops) if ops > 0 else 0.0
        avg_sequences_per_op = float(
            self._total_sequences / ops) if ops > 0 else 0.0
        overall_frac_full_bins = float(
            self._num_full_bins / total_bins) if total_bins > 0 else 0.0
        avg_packing_time = (
            float(self._total_packing_time / self._num_packing_time)
            if self._num_packing_time > 0
            else None
        )
        avg_utilization_per_op = float(
            self._sum_utilization_unweighted / ops) if ops > 0 else 0.0
        overall_coverage_ratio = (
            float(self._total_assigned_length / self._total_length)
            if self._total_length > 0
            else 1.0
        )

        stats: Dict[str, float] = {
            "operations": float(ops),
            "total_sequences": float(self._total_sequences),
            "total_bins": float(total_bins),
            "total_capacity": float(total_capacity),
            "total_length": float(self._total_length),
            "total_assigned_length": float(self._total_assigned_length),
            "total_effective_used_length": float(self._total_effective_used_length),
            "total_waste": float(self._total_waste),
            "total_overflow": float(self._total_overflow),
            "overall_utilization": overall_utilization,
            "overall_waste_ratio": overall_waste_ratio,
            "overall_coverage_ratio": overall_coverage_ratio,
            "overall_frac_full_bins": overall_frac_full_bins,
            "avg_std_fill_ratio": avg_std_fill_ratio,
            "avg_bins_per_op": avg_bins_per_op,
            "avg_sequences_per_op": avg_sequences_per_op,
            "avg_utilization_per_op": avg_utilization_per_op,
            "best_utilization": float(self._best_utilization) if self._best_utilization is not None else 0.0,
            "worst_utilization": float(self._worst_utilization) if self._worst_utilization is not None else 0.0,
        }
        if avg_packing_time is not None:
            stats["avg_packing_time"] = float(avg_packing_time)
            stats["num_packing_time_samples"] = float(self._num_packing_time)
            stats["total_packing_time"] = float(self._total_packing_time)

        return stats

    def print_aggregated_stats() -> None:
        """Print the aggregated metrics in a formatted way."""
        # This method signature must include self; correcting.
        raise NotImplementedError(
            "print_aggregated_stats requires an instance")


# Fixing the signature by defining the method properly below
def _packing_metrics_print_aggregated_stats(self) -> None:
    stats = self.get_aggregated_stats()

    def pct(x: float) -> str:
        return f"{x * 100:.2f}%"

    print("Packing Metrics (Aggregated):")
    print(f"  Operations: {int(stats.get('operations', 0))}")
    print(f"  Total sequences: {int(stats.get('total_sequences', 0))}")
    print(f"  Total bins: {int(stats.get('total_bins', 0))}")
    print(f"  Total capacity: {stats.get('total_capacity', 0.0):.2f}")
    print(
        f"  Total assigned length: {stats.get('total_assigned_length', 0.0):.2f}")
    print(
        f"  Total effective used length: {stats.get('total_effective_used_length', 0.0):.2f}")
    print(f"  Total waste: {stats.get('total_waste', 0.0):.2f}")
    print(f"  Total overflow: {stats.get('total_overflow', 0.0):.2f}")

    print(
        f"  Overall utilization: {pct(stats.get('overall_utilization', 0.0))}")
    print(
        f"  Overall waste ratio: {pct(stats.get('overall_waste_ratio', 0.0))}")
    print(
        f"  Overall coverage ratio: {pct(stats.get('overall_coverage_ratio', 0.0))}")
    print(
        f"  Fraction full bins (overall): {pct(stats.get('overall_frac_full_bins', 0.0))}")
    print(f"  Avg std fill ratio: {stats.get('avg_std_fill_ratio', 0.0):.4f}")
    print(f"  Avg bins/op: {stats.get('avg_bins_per_op', 0.0):.2f}")
    print(f"  Avg sequences/op: {stats.get('avg_sequences_per_op', 0.0):.2f}")
    print(
        f"  Avg utilization (unweighted per op): {pct(stats.get('avg_utilization_per_op', 0.0))}")
    print(f"  Best utilization: {pct(stats.get('best_utilization', 0.0))}")
    print(f"  Worst utilization: {pct(stats.get('worst_utilization', 0.0))}")
    if "avg_packing_time" in stats:
        print(f"  Avg packing time: {stats['avg_packing_time']:.6f}s "
              f"({int(stats.get('num_packing_time_samples', 0))} samples)")


# Attach the corrected method to the class
setattr(PackingMetrics, "print_aggregated_stats",
        _packing_metrics_print_aggregated_stats)


from typing import List, Dict, Optional


class PackingMetrics:
    """
    Collects and aggregates packing statistics over multiple runs.
    """

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        """Reset all aggregated statistics."""
        self.total_bins: int = 0
        self.total_items: int = 0
        self.total_length: int = 0
        self.total_utilization_sum: float = 0.0
        self.max_utilization: float = 0.0
        self.min_utilization: float = 1.0
        self.total_packing_time: float = 0.0
        self.num_updates: int = 0

    def update(
        self,
        sequence_lengths: List[int],
        bins: List[List[int]],
        bin_capacity: int,
        packing_time: Optional[float] = None,
    ) -> Dict[str, float]:
        """
        Update aggregated statistics with a new packing result.
        """
        stats = self.calculate_stats_only(sequence_lengths, bins, bin_capacity)
        if packing_time is not None:
            stats["packing_time"] = packing_time

        # Aggregate
        self.total_bins += stats["num_bins"]
        self.total_items += stats["total_items"]
        self.total_length += stats["total_length"]
        self.total_utilization_sum += stats["sum_utilization"]
        self.max_utilization = max(
            self.max_utilization, stats["max_utilization"])
        self.min_utilization = min(
            self.min_utilization, stats["min_utilization"])
        if packing_time is not None:
            self.total_packing_time += packing_time
        self.num_updates += 1

        # Return per-update stats
        return stats

    def calculate_stats_only(
        self, sequence_lengths: List[int], bins: List[List[int]], bin_capacity: int
    ) -> Dict[str, float]:
        """
        Calculate statistics for a single packing result without updating aggregates.
        """
        num_bins = len(bins)
        total_items = sum(len(b) for b in bins)
        total_length = sum(sum(b) for b in bins)

        # Utilization per bin
        utilizations = [
            sum(b) / bin_capacity if bin_capacity > 0 else 0.0 for b in bins
        ]
        sum_utilization = sum(utilizations)
        average_utilization = sum_utilization / num_bins if num_bins > 0 else 0.0
        max_utilization = max(utilizations) if utilizations else 0.0
        min_utilization = min(utilizations) if utilizations else 0.0
        average_items_per_bin = total_items / num_bins if num_bins > 0 else 0.0

        return {
            "num_bins": num_bins,
            "total_items": total_items,
            "total_length": total_length,
            "average_utilization": average_utilization,
            "max_utilization": max_utilization,
            "min_utilization": min_utilization,
            "average_items_per_bin": average_items_per_bin,
            "sum_utilization": sum_utilization,
        }

    def get_aggregated_stats(self) -> Dict[str, float]:
        """
        Return aggregated statistics across all updates.
        """
        if self.total_bins == 0:
            overall_average_utilization = 0.0
            average_items_per_bin = 0.0
        else:
            overall_average_utilization = self.total_utilization_sum / self.total_bins
            average_items_per_bin = self.total_items / self.total_bins

        average_packing_time = (
            self.total_packing_time / self.num_updates
            if self.num_updates > 0
            else None
        )

        return {
            "total_bins": self.total_bins,
            "total_items": self.total_items,
            "total_length": self.total_length,
            "overall_average_utilization": overall_average_utilization,
            "max_utilization": self.max_utilization,
            "min_utilization": self.min_utilization,
            "average_items_per_bin": average_items_per_bin,
            "total_packing_time": self.total_packing_time,
            "average_packing_time": average_packing_time,
        }

    def print_aggregated_stats(self) -> None:
        """
        Pretty‑print the aggregated statistics.
        """
        stats = self.get_aggregated_stats()
        print("Aggregated Packing Metrics:")
        print(f"  Total bins used: {stats['total_bins']}")
        print(f"  Total items packed: {stats['total_items']}")
        print(f"  Total length packed: {stats['total_length']}")
        print(
            f"  Overall average utilization: {stats['overall_average_utilization']:.4f}")
        print(f"  Max utilization: {stats['max_utilization']:.4f}")
        print(f"  Min utilization: {stats['min_utilization']:.4f}")
        print(f"  Average items per bin: {stats['average_items_per_bin']:.4f}")
        print(f"  Total packing time: {stats['total_packing_time']:.4f}s")
        if stats["average_packing_time"] is not None:
            print(
                f"  Average packing time: {stats['average_packing_time']:.4f}s")

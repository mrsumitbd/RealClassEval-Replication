
import subprocess
import re
import statistics
import platform
from typing import List, Tuple, Dict, Optional


class GCPRegions:
    '''
    A class for managing and analyzing Google Cloud Platform (GCP) regions.
    This class provides functionality to initialize, categorize, and analyze GCP regions based on their
    geographical location, tier classification, and network latency.
    Attributes:
        regions (Dict[str, Tuple[int, str, str]]): A dictionary of GCP regions with their tier, city, and country.
    Methods:
        tier1: Returns a list of tier 1 GCP regions.
        tier2: Returns a list of tier 2 GCP regions.
        lowest_latency: Determines the GCP region(s) with the lowest network latency.
    Examples:
        >>> from ultralytics.hub.google import GCPRegions
        >>> regions = GCPRegions()
        >>> lowest_latency_region = regions.lowest_latency(verbose=True, attempts=3)
        >>> print(f"Lowest latency region: {lowest_latency_region[0][0]}")
    '''

    def __init__(self):
        # Sample data: (tier, city, country)
        self.regions: Dict[str, Tuple[int, str, str]] = {
            'us-central1': (1, 'Iowa', 'USA'),
            'us-east1': (1, 'South Carolina', 'USA'),
            'us-west1': (1, 'Oregon', 'USA'),
            'europe-west1': (2, 'Belgium', 'Belgium'),
            'europe-west2': (2, 'London', 'UK'),
            'asia-east1': (2, 'Taiwan', 'Taiwan'),
            'asia-northeast1': (2, 'Tokyo', 'Japan'),
            'southamerica-east1': (2, 'Sao Paulo', 'Brazil'),
            'australia-southeast1': (2, 'Singapore', 'Singapore'),
            'northamerica-northeast1': (1, 'Montreal', 'Canada')
        }

    def tier1(self) -> List[str]:
        return [region for region, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        return [region for region, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        """
        Ping a region name (treated as a hostname) and return latency statistics.
        Returns a tuple: (region, mean_latency, std_dev, min_latency, max_latency)
        """
        if attempts < 1:
            attempts = 1

        # Determine ping command based on OS
        if platform.system().lower() == 'windows':
            cmd = ['ping', '-n', str(attempts), '-w', '1000', region]
        else:
            cmd = ['ping', '-c', str(attempts), '-W', '1', region]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=attempts * 2
            )
            output = result.stdout
            # Extract all time=XX ms values
            times = [float(m.group(1)) for m in re.finditer(
                r'time[=<]([0-9.]+)\s*ms', output)]
            if not times:
                # No successful pings; treat as high latency
                return (region, 9999.0, 0.0, 9999.0, 9999.0)
            mean_latency = statistics.mean(times)
            std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
            min_latency = min(times)
            max_latency = max(times)
            return (region, mean_latency, std_dev, min_latency, max_latency)
        except Exception:
            # On any error, return high latency
            return (region, 9999.0, 0.0, 9999.0, 9999.0)

    def lowest_latency(
        self,
        top: int = 1,
        verbose: bool = False,
        tier: Optional[int] = None,
        attempts: int = 1
    ) -> List[Tuple[str, float, float, float, float]]:
        """
        Determines the GCP regions with the lowest latency based on ping tests.
        Args:
            top (int): Number of top regions to return.
            verbose (bool): If True, prints detailed latency information for all tested regions.
            tier (int | None): Filter regions by tier (1 or 2). If None, all regions are tested.
            attempts (int): Number of ping attempts per region.
        Returns:
            (List[Tuple[str, float, float, float, float]]): List of tuples containing region information and
            latency statistics. Each tuple contains (region, mean_latency, std_dev, min_latency, max_latency).
        """
        if tier is not None and tier not in (1, 2):
            raise ValueError("tier must be 1, 2, or None")

        # Filter regions by tier if requested
        candidate_regions = [
            region for region, (reg_tier, _, _) in self.regions.items()
            if tier is None or reg_tier == tier
        ]

        results: List[Tuple[str, float, float, float, float]] = []

        for region in candidate_regions:
            stats = self._ping_region(region, attempts)
            results.append(stats)

        if verbose:
            print(
                f"{'Region':<20} {'Mean(ms)':>10} {'StdDev(ms)':>12} {'Min(ms)':>10} {'Max(ms)':>10}")
            for r in results:
                print(
                    f"{r[0]:<20} {r[1]:>10.2f} {r[2]:>12.2f} {r[3]:>10.2f} {r[4]:>10.2f}")

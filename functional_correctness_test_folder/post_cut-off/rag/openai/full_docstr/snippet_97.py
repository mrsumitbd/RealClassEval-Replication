
import subprocess
import re
import statistics
import platform
from typing import Dict, Tuple, List, Optional


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
        '''Initializes the GCPRegions class with predefined Google Cloud Platform regions and their details.'''
        # Sample data – in a real implementation this would be more exhaustive
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # tier 1
            'us-central1': (1, 'Iowa', 'USA'),
            'us-east1': (1, 'South Carolina', 'USA'),
            'us-west1': (1, 'Oregon', 'USA'),
            'europe-west1': (1, 'Belgium', 'Belgium'),
            'asia-east1': (1, 'Taiwan', 'Taiwan'),
            # tier 2
            'asia-northeast1': (2, 'Tokyo', 'Japan'),
            'asia-south1': (2, 'Mumbai', 'India'),
            'europe-west2': (2, 'London', 'UK'),
            'southamerica-east1': (2, 'Sao Paulo', 'Brazil'),
            'australia-southeast1': (2, 'Sydney', 'Australia'),
        }

    def tier1(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 1 based on predefined criteria.'''
        return [r for r, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 2 based on predefined criteria.'''
        return [r for r, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        '''Pings a specified GCP region and returns latency statistics: mean, min, max, and standard deviation.'''
        # Use the region name as a host – many GCP region names resolve to a public IP
        host = region
        system = platform.system()
        if system == 'Windows':
            cmd = ['ping', '-n', str(attempts), '-w', '1000', host]
        else:
            # Unix-like
            cmd = ['ping', '-c', str(attempts), '-W', '1', host]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=attempts * 2,
            )
            output = result.stdout + result.stderr
            # Extract all latency numbers (ms)
            # Linux: time=XX ms
            # Windows: Average = XXms
            times = [float(m) for m in re.findall(
                r'time[=<]([\d\.]+)\s*ms', output, re.IGNORECASE)]
            if not times:
                # Try Windows style
                times = [float(m) for m in re.findall(
                    r'Average = ([\d\.]+)ms', output, re.IGNORECASE)]
            if not times:
                # No ping data – treat as failure
                return (region, float('inf'), 0.0, 0.0, 0.0)
            mean = statistics.mean(times)
            min_t = min(times)
            max_t = max(times)
            std = statistics.stdev(times) if len(times) > 1 else 0.0
            return (region, mean, std, min_t, max_t)
        except Exception:
            # Any error – return infinite latency
            return (region, float('inf'), 0.0, 0.0, 0.0)

    def lowest_latency(
        self,
        top: int = 1,
        verbose: bool = False,
        tier: Optional[int] = None,
        attempts: int = 1,
    ) -> List[Tuple[str, float, float, float, float]]:
        '''
        Determines the GCP regions with the lowest latency based on ping tests.
        Args:
            top (int): Number of top regions to return.
            verbose (bool): If True, prints detailed latency information for all tested regions.
            tier (int | None): Filter regions by tier (1 or 2). If None, all regions are tested.
            attempts (int): Number of ping attempts per region.
        Returns:
            (List[Tuple[str, float, float, float, float]]): List of tuples containing region information and
            latency statistics. Each tuple contains (region, mean_latency, std_dev, min_latency, max_latency).
        Examples:
            >>> regions = GCPRegions()
            >>> results = regions.lowest_latency(top=3, verbose=True, tier=1, attempts=2)
            >>> print(results[0][0])  # Print the name of the lowest latency region
        '''
        # Filter regions by tier if requested
        if tier is not None:
            candidates = [
                r for r, (t, _, _) in self.regions.items() if t == tier]
        else:
            candidates = list(self.regions.keys())

        stats = []
        for region in candidates:
            stat = self._ping_region(region, attempts=attempts)
            stats.append(stat)
            if verbose:
                print(
                    f"{region:15s} mean={stat[1]:.2f}ms std={stat[2]:.2f}ms min={stat[3]:.2f}ms max={stat[4]:.2f}ms")

        # Sort by mean latency (ascending)
        stats.sort(key=lambda x: x[1])
        return stats[:top]

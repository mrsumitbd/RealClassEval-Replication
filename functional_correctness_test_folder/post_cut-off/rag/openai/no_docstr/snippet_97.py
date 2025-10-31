
import os
import re
import subprocess
import sys
import math
import statistics
from typing import Dict, List, Tuple, Optional


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
        # tier, city, country
        self.regions: Dict[str, Tuple[int, str, str]] = {
            'us-central1': (1, 'Iowa', 'USA'),
            'us-east1': (1, 'South Carolina', 'USA'),
            'us-west1': (1, 'Oregon', 'USA'),
            'europe-west1': (1, 'Belgium', 'Belgium'),
            'asia-east1': (1, 'Taiwan', 'Taiwan'),
            'asia-northeast1': (2, 'Tokyo', 'Japan'),
            'asia-south1': (2, 'Mumbai', 'India'),
            'australia-southeast1': (2, 'Sydney', 'Australia'),
            'southamerica-east1': (2, 'Sao Paulo', 'Brazil')
        }

    def tier1(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 1 based on predefined criteria.'''
        return [region for region, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 2 based on predefined criteria.'''
        return [region for region, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        '''Pings a specified GCP region and returns latency statistics: mean, min, max, and standard deviation.'''
        # Determine ping command based on OS
        if sys.platform.startswith('win'):
            ping_cmd = ['ping', '-n', str(attempts), region]
        else:
            ping_cmd = ['ping', '-c', str(attempts), region]

        try:
            result = subprocess.run(
                ping_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=attempts * 5
            )
            output = result.stdout
            # Extract times
            times = [float(m.group(1))
                     for m in re.finditer(r'time[=<]([\d\.]+)', output)]
            if not times:
                # Try Windows style 'time=12ms' or 'time<12ms'
                times = [float(m.group(1))
                         for m in re.finditer(r'time[=<]([\d\.]+)ms', output)]
            if not times:
                # No ping results
                return (region, math.inf, math.inf, math.inf, math.inf)
            mean = statistics.mean(times)
            min_latency = min(times)
            max_latency = max(times)
            std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
            return (region, mean, std_dev, min_latency, max_latency)
        except Exception:
            return (region, math.inf, math.inf, math.inf, math.inf)

    def lowest_latency(
        self,
        top: int = 1,
        verbose: bool = False,
        tier: Optional[int] = None,
        attempts: int = 1
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
            region_list = [
                r for r, (t, _, _) in self.regions.items() if t == tier]
        else:
            region_list = list(self.regions.keys())

        latency_results: List[Tuple[str, float, float, float, float]] =

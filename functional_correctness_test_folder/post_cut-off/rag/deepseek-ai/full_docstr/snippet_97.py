
from typing import Dict, List, Tuple, Optional
import subprocess
import statistics


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
        self.regions = {
            'us-central1': (1, 'Council Bluffs', 'USA'),
            'us-east1': (1, 'Moncks Corner', 'USA'),
            'us-west1': (1, 'The Dalles', 'USA'),
            'europe-west1': (1, 'St. Ghislain', 'Belgium'),
            'asia-east1': (1, 'Changhua County', 'Taiwan'),
            'asia-northeast1': (1, 'Tokyo', 'Japan'),
            'asia-southeast1': (2, 'Jurong West', 'Singapore'),
            'australia-southeast1': (2, 'Sydney', 'Australia'),
            'southamerica-east1': (2, 'São Paulo', 'Brazil'),
            'europe-west4': (2, 'Eemshaven', 'Netherlands'),
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
        host = f'{region}.googleapis.com'
        latencies = []
        for _ in range(attempts):
            try:
                result = subprocess.run(
                    ['ping', '-c', '1', host], capture_output=True, text=True, timeout=5)
                if 'time=' in result.stdout:
                    time_str = result.stdout.split('time=')[1].split(' ')[0]
                    latencies.append(float(time_str))
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                continue
        if not latencies:
            return (region, float('inf'), 0.0, float('inf'), float('inf'))
        mean = statistics.mean(latencies)
        std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
        min_latency = min(latencies)
        max_latency = max(latencies)
        return (region, mean, std_dev, min_latency, max_latency)

    def lowest_latency(self, top: int = 1, verbose: bool = False, tier: Optional[int] = None, attempts: int = 1) -> List[Tuple[str, float, float, float, float]]:
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
        regions_to_test = []
        if tier is None:
            regions_to_test = list(self.regions.keys())
        elif tier == 1:
            regions_to_test = self.tier1()
        elif tier == 2:
            regions_to_test = self.tier2()
        else:
            raise ValueError('Tier must be 1, 2, or None.')

        results = []
        for region in regions_to_test:
            result = self._ping_region(region, attempts)
            results.append(result)
            if verbose:
                print(
                    f'Region: {result[0]}, Mean Latency: {result[1]:.2f}ms, Std Dev: {result[2]:.2f}ms, Min: {result[3]:.2f}ms, Max: {result[4]:.2f}ms')

        results.sort(key=lambda x: x[1])
        return results[:top]

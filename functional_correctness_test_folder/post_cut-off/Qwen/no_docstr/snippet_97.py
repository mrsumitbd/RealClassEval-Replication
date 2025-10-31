
from typing import List, Tuple, Dict, Optional
import statistics
import subprocess


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
        self.regions = {
            'us-central1': (1, 'Council Bluffs', 'USA'),
            'europe-west1': (1, 'St. Ghislain', 'Belgium'),
            'asia-east1': (1, 'Changhua County', 'Taiwan'),
            'us-west1': (2, 'The Dalles', 'USA'),
            'europe-west2': (2, 'London', 'UK'),
            'asia-northeast1': (2, 'Tokyo', 'Japan')
        }

    def tier1(self) -> List[str]:
        return [region for region, (tier, city, country) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        return [region for region, (tier, city, country) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        latencies = []
        for _ in range(attempts):
            try:
                output = subprocess.check_output(
                    ['ping', '-c', '1', f'{region}.google.com'], universal_newlines=True)
                latency = float(output.split('time=')[1].split(' ms')[0])
                latencies.append(latency)
            except (subprocess.CalledProcessError, IndexError):
                latencies.append(float('inf'))
        mean_latency = statistics.mean(latencies)
        std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
        min_latency = min(latencies)
        max_latency = max(latencies)
        return region, mean_latency, std_dev, min_latency, max_latency

    def lowest_latency(self, top: int = 1, verbose: bool = False, tier: Optional[int] = None, attempts: int = 1) -> List[Tuple[str, float, float, float, float]]:
        regions_to_test = self.regions.keys() if tier is None else (
            self.tier1() if tier == 1 else self.tier2())
        results = [self._ping_region(region, attempts)
                   for region in regions_to_test]
        results.sort(key=lambda x: x[1])
        if verbose:
            for region, mean_latency, std_dev, min_latency, max_latency in results:
                print(
                    f"Region: {region}, Mean Latency: {mean_latency:.2f} ms, Std Dev: {std_dev:.2f} ms, Min: {min_latency:.2f} ms, Max: {max_latency:.2f} ms")
        return results[:top]

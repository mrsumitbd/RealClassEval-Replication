
from typing import List, Tuple, Optional
import subprocess
import re
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
            'us-east4': (1, 'Ashburn', 'USA'),
            'us-west1': (1, 'The Dalles', 'USA'),
            'us-west2': (1, 'Los Angeles', 'USA'),
            'us-west3': (1, 'Salt Lake City', 'USA'),
            'us-west4': (1, 'Las Vegas', 'USA'),
            'europe-west1': (1, 'St. Ghislain', 'Belgium'),
            'europe-west2': (1, 'London', 'UK'),
            'europe-west3': (1, 'Frankfurt', 'Germany'),
            'europe-west4': (1, 'Eemshaven', 'Netherlands'),
            'europe-west6': (1, 'Zürich', 'Switzerland'),
            'europe-central2': (1, 'Warsaw', 'Poland'),
            'europe-north1': (1, 'Hamina', 'Finland'),
            'asia-east1': (1, 'Changhua County', 'Taiwan'),
            'asia-east2': (1, 'Hong Kong', 'Hong Kong'),
            'asia-northeast1': (1, 'Tokyo', 'Japan'),
            'asia-northeast2': (1, 'Osaka', 'Japan'),
            'asia-northeast3': (1, 'Seoul', 'South Korea'),
            'asia-south1': (1, 'Mumbai', 'India'),
            'asia-south2': (1, 'Delhi', 'India'),
            'asia-southeast1': (1, 'Jurong West', 'Singapore'),
            'asia-southeast2': (1, 'Jakarta', 'Indonesia'),
            'australia-southeast1': (1, 'Sydney', 'Australia'),
            'australia-southeast2': (1, 'Melbourne', 'Australia'),
            'southamerica-east1': (1, 'Osasco', 'Brazil'),
            'southamerica-west1': (1, 'Santiago', 'Chile'),
            'northamerica-northeast1': (2, 'Montréal', 'Canada'),
            'northamerica-northeast2': (2, 'Toronto', 'Canada'),
            'southamerica-east1': (2, 'Osasco', 'Brazil'),
            'southamerica-west1': (2, 'Santiago', 'Chile'),
            'europe-west8': (2, 'Milan', 'Italy'),
            'europe-west9': (2, 'Paris', 'France'),
            'europe-west10': (2, 'Berlin', 'Germany'),
            'europe-west12': (2, 'Amsterdam', 'Netherlands'),
            'europe-southwest1': (2, 'Madrid', 'Spain'),
            'me-west1': (2, 'Tel Aviv', 'Israel'),
            'africa-south1': (2, 'Cape Town', 'South Africa'),
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
        host = f"{region}-gcp.ultralytics.com"
        latencies = []

        for _ in range(attempts):
            try:
                output = subprocess.check_output(
                    ['ping', '-c', '1', host], stderr=subprocess.STDOUT, universal_newlines=True)
                match = re.search(r'time=([\d.]+) ms', output)
                if match:
                    latency = float(match.group(1))
                    latencies.append(latency)
            except subprocess.CalledProcessError:
                continue

        if not latencies:
            return (region, float('inf'), float('inf'), float('inf'), float('inf'))

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
        regions_to_test = self.regions.keys()
        if tier is not None:
            regions_to_test = self.tier1() if tier == 1 else self.tier2()

        results = []
        for region in regions_to_test:
            result = self._ping_region(region, attempts)
            results.append(result)
            if verbose:
                print(
                    f"Region: {result[0]}, Mean: {result[1]:.2f} ms, Std Dev: {result[2]:.2f} ms, Min: {result[3]:.2f} ms, Max: {result[4]:.2f} ms")

        results.sort(key=lambda x: x[1])
        return results[:top]

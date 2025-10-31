
import subprocess
import statistics
from typing import List, Tuple, Optional, Dict


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
            'us-east1': (1, 'Moncks Corner', 'USA'),
            'us-east4': (1, 'Ashburn', 'USA'),
            'us-west1': (1, 'The Dalles', 'USA'),
            'us-west2': (1, 'Council Bluffs', 'USA'),
            'us-west3': (1, 'Salt Lake City', 'USA'),
            'us-west4': (1, 'Las Vegas', 'USA'),
            'europe-west1': (1, 'St. Ghislain', 'Belgium'),
            'europe-west2': (1, 'London', 'UK'),
            'europe-west3': (1, 'Frankfurt', 'Germany'),
            'europe-west4': (1, 'Eemshaven', 'Netherlands'),
            'europe-west6': (1, 'Zürich', 'Switzerland'),
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
            'southamerica-east2': (2, 'São Paulo', 'Brazil'),
            'southamerica-west2': (2, 'Buenos Aires', 'Argentina'),
            'europe-central2': (2, 'Warsaw', 'Poland'),
            'europe-west8': (2, 'Milan', 'Italy'),
            'europe-west9': (2, 'Paris', 'France'),
            'europe-west10': (2, 'Berlin', 'Germany'),
            'europe-west12': (2, 'Västerås', 'Sweden'),
            'me-west1': (2, 'Tel Aviv', 'Israel'),
            'me-central1': (2, 'Doha', 'Qatar'),
            'asia-east3': (2, 'Changhua County', 'Taiwan'),
            'asia-southeast3': (2, 'Kuala Lumpur', 'Malaysia'),
            'asia-southeast4': (2, 'Singapore', 'Singapore'),
            'asia-northeast4': (2, 'Tokyo', 'Japan'),
            'asia-south3': (2, 'Mumbai', 'India'),
            'australia-southeast3': (2, 'Sydney', 'Australia'),
            'australia-southeast4': (2, 'Melbourne', 'Australia'),
        }

    def tier1(self) -> List[str]:
        return [region for region, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        return [region for region, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        latencies = []
        for _ in range(attempts):
            try:
                output = subprocess.check_output(
                    ['ping', '-c', '1', f'{region}.googleapis.com'], stderr=subprocess.STDOUT, universal_newlines=True)
                latency = float(output.split('time=')[1].split(' ')[0])
                latencies.append(latency)
            except subprocess.CalledProcessError as e:
                print(f"Error pinging {region}: {e.output}")
                latencies.append(float('inf'))

        mean_latency = statistics.mean(latencies)
        std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
        min_latency = min(latencies)
        max_latency = max(latencies)

        return (region, mean_latency, std_dev, min_latency, max_latency)

    def lowest_latency(self, top: int = 1, verbose: bool = False, tier: Optional[int] = None, attempts: int = 1) -> List[Tuple[str, float, float, float, float]]:
        regions_to_test = self.regions.keys()
        if tier is not None:
            regions_to_test = self.tier1() if tier == 1 else self.tier2()

        results = []
        for region in regions_to_test:
            result = self._ping_region(region, attempts)
            results.append(result)
            if verbose:
                print(
                    f"Region: {result[0]}, Mean Latency: {result[1]:.2f} ms, Std Dev: {result[2]:.2f} ms, Min Latency: {result[3]:.2f} ms, Max Latency: {result[4]:.2f} ms")

        results.sort(key=lambda x: x[1])
        return results[:top]

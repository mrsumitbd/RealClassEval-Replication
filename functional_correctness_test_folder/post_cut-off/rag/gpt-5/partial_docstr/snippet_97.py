from typing import Dict, List, Optional, Tuple
from time import perf_counter
import random
import urllib.request
import urllib.error
import math


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
        tier1_set = {
            'us-central1', 'us-east1', 'us-west1',
            'europe-west1', 'europe-west4',
            'asia-east1', 'asia-southeast1',
            'asia-northeast1'
        }
        all_regions: Dict[str, Tuple[int, str, str]] = {
            # Americas
            'us-central1': (1 if 'us-central1' in tier1_set else 2, 'Iowa', 'USA'),
            'us-east1': (1 if 'us-east1' in tier1_set else 2, 'South Carolina', 'USA'),
            'us-east4': (2, 'Northern Virginia', 'USA'),
            'us-west1': (1 if 'us-west1' in tier1_set else 2, 'Oregon', 'USA'),
            'us-west2': (2, 'Los Angeles', 'USA'),
            'us-west3': (2, 'Salt Lake City', 'USA'),
            'us-west4': (2, 'Las Vegas', 'USA'),
            'northamerica-northeast1': (2, 'Montreal', 'Canada'),
            'northamerica-northeast2': (2, 'Toronto', 'Canada'),
            'southamerica-east1': (2, 'São Paulo', 'Brazil'),
            'southamerica-west1': (2, 'Santiago', 'Chile'),
            # Europe
            'europe-west1': (1 if 'europe-west1' in tier1_set else 2, 'Belgium', 'Belgium'),
            'europe-west2': (2, 'London', 'United Kingdom'),
            'europe-west3': (2, 'Frankfurt', 'Germany'),
            'europe-west4': (1 if 'europe-west4' in tier1_set else 2, 'Netherlands', 'Netherlands'),
            'europe-west6': (2, 'Zurich', 'Switzerland'),
            'europe-west8': (2, 'Milan', 'Italy'),
            'europe-west9': (2, 'Paris', 'France'),
            'europe-north1': (2, 'Hamina', 'Finland'),
            'europe-central2': (2, 'Warsaw', 'Poland'),
            'europe-southwest1': (2, 'Madrid', 'Spain'),
            # Asia Pacific
            'asia-east1': (1 if 'asia-east1' in tier1_set else 2, 'Changhua County', 'Taiwan'),
            'asia-east2': (2, 'Hong Kong', 'China'),
            'asia-northeast1': (1 if 'asia-northeast1' in tier1_set else 2, 'Tokyo', 'Japan'),
            'asia-northeast2': (2, 'Osaka', 'Japan'),
            'asia-northeast3': (2, 'Seoul', 'South Korea'),
            'asia-south1': (2, 'Mumbai', 'India'),
            'asia-south2': (2, 'Delhi', 'India'),
            'asia-southeast1': (1 if 'asia-southeast1' in tier1_set else 2, 'Singapore', 'Singapore'),
            'asia-southeast2': (2, 'Jakarta', 'Indonesia'),
            # Australia
            'australia-southeast1': (2, 'Sydney', 'Australia'),
            'australia-southeast2': (2, 'Melbourne', 'Australia'),
            # Middle East
            'me-central1': (2, 'Doha', 'Qatar'),
            'me-central2': (2, 'Dammam', 'Saudi Arabia'),
            'me-west1': (2, 'Tel Aviv', 'Israel'),
            # Africa
            'africa-south1': (2, 'Johannesburg', 'South Africa'),
        }
        self.regions: Dict[str, Tuple[int, str, str]] = all_regions

    def tier1(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 1 based on predefined criteria.'''
        return [r for r, (t, _, _) in self.regions.items() if t == 1]

    def tier2(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 2 based on predefined criteria.'''
        return [r for r, (t, _, _) in self.regions.items() if t == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        '''Pings a specified GCP region and returns latency statistics: mean, min, max, and standard deviation.'''
        attempts = max(1, int(attempts))
        url_base = f"https://{region}.gcping.com/ping"
        latencies_ms: List[float] = []
        for i in range(attempts):
            ts = f"{perf_counter():.9f}"
            nonce = random.randint(0, 1_000_000)
            url = f"{url_base}?n={i}&t={ts}&r={nonce}"
            start = perf_counter()
            try:
                req = urllib.request.Request(
                    url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    # read minimal payload to ensure completion
                    _ = resp.read(8)
                elapsed_ms = (perf_counter() - start) * 1000.0
                latencies_ms.append(elapsed_ms)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError):
                latencies_ms.append(float('inf'))
        finite_vals = [x for x in latencies_ms if math.isfinite(x)]
        if not finite_vals:
            mean_v = std_v = min_v = max_v = float('inf')
        else:
            mean_v = sum(finite_vals) / len(finite_vals)
            min_v = min(finite_vals)
            max_v = max(finite_vals)
            if len(finite_vals) == 1:
                std_v = 0.0
            else:
                var = sum((x - mean_v) ** 2 for x in finite_vals) / \
                    len(finite_vals)
                std_v = math.sqrt(var)
        return region, mean_v, std_v, min_v, max_v

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
        if tier not in (None, 1, 2):
            raise ValueError("tier must be None, 1, or 2")
        if tier == 1:
            region_list = self.tier1()
        elif tier == 2:
            region_list = self.tier2()
        else:
            region_list = list(self.regions.keys())

        results: List[Tuple[str, float, float, float, float]] = []
        for r in region_list:
            res = self._ping_region(r, attempts=attempts)
            results.append(res)

        # Sort by mean latency ascending; infinities go to the end
        results.sort(key=lambda x: (math.isfinite(x[1]) == False, x[1]))

        if verbose:
            print("GCP region latency (ms):")
            for region, mean_v, std_v, min_v, max_v in results:
                tier_val = self.regions.get(region, (None, '', ''))[0]
                city, country = self.regions.get(region, (0, '', ''))[1:]
                if math.isfinite(mean_v):
                    print(
                        f"- {region} (Tier {tier_val}, {city}, {country}): mean={mean_v:.2f}, std={std_v:.2f}, min={min_v:.2f}, max={max_v:.2f}")
                else:
                    print(
                        f"- {region} (Tier {tier_val}, {city}, {country}): unreachable")

        top_n = max(1, int(top))
        return results[:top_n]

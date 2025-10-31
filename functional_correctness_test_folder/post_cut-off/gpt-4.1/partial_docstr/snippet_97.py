
import subprocess
import sys
import platform
import statistics
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
    # GCP region endpoints for pinging
    _region_endpoints = {
        # region: endpoint
        'asia-east1': 'asia-east1-a.gce.cloud.google.com',
        'asia-east2': 'asia-east2-a.gce.cloud.google.com',
        'asia-northeast1': 'asia-northeast1-a.gce.cloud.google.com',
        'asia-northeast2': 'asia-northeast2-a.gce.cloud.google.com',
        'asia-northeast3': 'asia-northeast3-a.gce.cloud.google.com',
        'asia-south1': 'asia-south1-a.gce.cloud.google.com',
        'asia-south2': 'asia-south2-a.gce.cloud.google.com',
        'asia-southeast1': 'asia-southeast1-a.gce.cloud.google.com',
        'asia-southeast2': 'asia-southeast2-a.gce.cloud.google.com',
        'australia-southeast1': 'australia-southeast1-a.gce.cloud.google.com',
        'australia-southeast2': 'australia-southeast2-a.gce.cloud.google.com',
        'europe-central2': 'europe-central2-a.gce.cloud.google.com',
        'europe-north1': 'europe-north1-a.gce.cloud.google.com',
        'europe-west1': 'europe-west1-a.gce.cloud.google.com',
        'europe-west2': 'europe-west2-a.gce.cloud.google.com',
        'europe-west3': 'europe-west3-a.gce.cloud.google.com',
        'europe-west4': 'europe-west4-a.gce.cloud.google.com',
        'europe-west6': 'europe-west6-a.gce.cloud.google.com',
        'northamerica-northeast1': 'northamerica-northeast1-a.gce.cloud.google.com',
        'northamerica-northeast2': 'northamerica-northeast2-a.gce.cloud.google.com',
        'southamerica-east1': 'southamerica-east1-a.gce.cloud.google.com',
        'southamerica-west1': 'southamerica-west1-a.gce.cloud.google.com',
        'us-central1': 'us-central1-a.gce.cloud.google.com',
        'us-east1': 'us-east1-a.gce.cloud.google.com',
        'us-east4': 'us-east4-a.gce.cloud.google.com',
        'us-east5': 'us-east5-a.gce.cloud.google.com',
        'us-south1': 'us-south1-a.gce.cloud.google.com',
        'us-west1': 'us-west1-a.gce.cloud.google.com',
        'us-west2': 'us-west2-a.gce.cloud.google.com',
        'us-west3': 'us-west3-a.gce.cloud.google.com',
        'us-west4': 'us-west4-a.gce.cloud.google.com',
        'me-central1': 'me-central1-a.gce.cloud.google.com',
        'me-west1': 'me-west1-a.gce.cloud.google.com',
    }

    def __init__(self):
        '''Initializes the GCPRegions class with predefined Google Cloud Platform regions and their details.'''
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # region: (tier, city, country)
            'asia-east1': (1, 'Changhua County', 'Taiwan'),
            'asia-east2': (2, 'Hong Kong', 'Hong Kong'),
            'asia-northeast1': (1, 'Tokyo', 'Japan'),
            'asia-northeast2': (2, 'Osaka', 'Japan'),
            'asia-northeast3': (2, 'Seoul', 'South Korea'),
            'asia-south1': (2, 'Mumbai', 'India'),
            'asia-south2': (2, 'Delhi', 'India'),
            'asia-southeast1': (2, 'Jurong West', 'Singapore'),
            'asia-southeast2': (2, 'Jakarta', 'Indonesia'),
            'australia-southeast1': (2, 'Sydney', 'Australia'),
            'australia-southeast2': (2, 'Melbourne', 'Australia'),
            'europe-central2': (2, 'Warsaw', 'Poland'),
            'europe-north1': (2, 'Hamina', 'Finland'),
            'europe-west1': (1, 'St. Ghislain', 'Belgium'),
            'europe-west2': (2, 'London', 'UK'),
            'europe-west3': (2, 'Frankfurt', 'Germany'),
            'europe-west4': (2, 'Eemshaven', 'Netherlands'),
            'europe-west6': (2, 'Zurich', 'Switzerland'),
            'northamerica-northeast1': (2, 'Montreal', 'Canada'),
            'northamerica-northeast2': (2, 'Toronto', 'Canada'),
            'southamerica-east1': (2, 'Osasco', 'Brazil'),
            'southamerica-west1': (2, 'Santiago', 'Chile'),
            'us-central1': (1, 'Council Bluffs', 'Iowa, USA'),
            'us-east1': (1, 'Moncks Corner', 'South Carolina, USA'),
            'us-east4': (2, 'Ashburn', 'N. Virginia, USA'),
            'us-east5': (2, 'Columbus', 'Ohio, USA'),
            'us-south1': (2, 'Dallas', 'Texas, USA'),
            'us-west1': (1, 'The Dalles', 'Oregon, USA'),
            'us-west2': (2, 'Los Angeles', 'California, USA'),
            'us-west3': (2, 'Salt Lake City', 'Utah, USA'),
            'us-west4': (2, 'Las Vegas', 'Nevada, USA'),
            'me-central1': (2, 'Doha', 'Qatar'),
            'me-west1': (2, 'Tel Aviv', 'Israel'),
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
        endpoint = GCPRegions._region_endpoints.get(region)
        if endpoint is None:
            raise ValueError(f"Unknown region: {region}")

        latencies = []
        for _ in range(attempts):
            try:
                if platform.system().lower() == "windows":
                    # Windows: ping -n <count> -w <timeout_ms> <host>
                    cmd = ["ping", "-n", "1", "-w", "1000", endpoint]
                else:
                    # Unix: ping -c <count> -W <timeout_sec> <host>
                    cmd = ["ping", "-c", "1", "-W", "1", endpoint]
                proc = subprocess.run(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = proc.stdout
                # Parse latency from output
                if platform.system().lower() == "windows":
                    # Look for "Average = XXms"
                    for line in output.splitlines():
                        if "Average =" in line:
                            latency_str = line.split("Average =")[-1].strip()
                            if latency_str.endswith("ms"):
                                latency = float(
                                    latency_str.replace("ms", "").strip())
                                latencies.append(latency)
                else:
                    # Look for "time=XX ms"
                    for line in output.splitlines():
                        if "time=" in line:
                            idx = line.find("time=")
                            if idx != -1:
                                time_part = line[idx+5:]
                                ms_idx = time_part.find(" ms")
                                if ms_idx != -1:
                                    latency = float(time_part[:ms_idx].strip())
                                    latencies.append(latency)
            except Exception:
                continue

        if not latencies:
            # If all pings failed, set to a high latency
            return (region, float('inf'), float('inf'), float('inf'), float('inf'))

        mean = statistics.mean(latencies)
        stddev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
        min_latency = min(latencies)
        max_latency = max(latencies)
        return (region, mean, stddev, min_latency, max_latency)

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
        if tier is not None:
            regions = [r for r, (t, _, _) in self.regions.items() if t == tier]
        else:
            regions = list(self.regions.keys())

        results = []
        for region in regions:
            stats = self._ping_region(region, attempts=attempts)
            results.append(stats)

        # Sort by mean latency
        results.sort(key=lambda x: x[1])
        if verbose:
            print("Region\t\tMean(ms)\tStdDev\tMin\tMax")
            for r in results:
                print(
                    f"{r[0]:<20} {r[1]:.2f}\t{r[2]:.2f}\t{r[3]:.2f}\t{r[4]:.2f}")
        return results[:top]


import os
import platform
import subprocess
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

    def __init__(self):
        # Initialize GCP regions dictionary
        self.regions = {
            'asia-east1': (1, 'Taiwan', 'Taiwan'),
            'asia-east2': (2, 'Hong Kong', 'Hong Kong'),
            'asia-northeast1': (1, 'Tokyo', 'Japan'),
            'asia-northeast2': (2, 'Osaka', 'Japan'),
            'asia-northeast3': (2, 'Seoul', 'South Korea'),
            'asia-south1': (1, 'Mumbai', 'India'),
            'asia-south2': (2, 'Delhi', 'India'),
            'asia-southeast1': (1, 'Singapore', 'Singapore'),
            'asia-southeast2': (2, 'Jakarta', 'Indonesia'),
            'australia-southeast1': (1, 'Sydney', 'Australia'),
            'australia-southeast2': (2, 'Melbourne', 'Australia'),
            'europe-central2': (2, 'Warsaw', 'Poland'),
            'europe-north1': (1, 'Finland', 'Finland'),
            'europe-southwest1': (1, 'Madrid', 'Spain'),
            'europe-west1': (1, 'Belgium', 'Belgium'),
            'europe-west2': (2, 'London', 'United Kingdom'),
            'europe-west3': (2, 'Frankfurt', 'Germany'),
            'europe-west4': (1, 'Netherlands', 'Netherlands'),
            'europe-west6': (2, 'Zurich', 'Switzerland'),
            'europe-west8': (2, 'Milan', 'Italy'),
            'europe-west9': (2, 'Paris', 'France'),
            'northamerica-northeast1': (1, 'Montreal', 'Canada'),
            'northamerica-northeast2': (2, 'Toronto', 'Canada'),
            'southamerica-east1': (1, 'Sao Paulo', 'Brazil'),
            'southamerica-west1': (1, 'Santiago', 'Chile'),
            'us-central1': (1, 'Iowa', 'United States'),
            'us-east1': (1, 'South Carolina', 'United States'),
            'us-east4': (1, 'Northern Virginia', 'United States'),
            'us-east5': (2, 'Columbus', 'United States'),
            'us-south1': (1, 'Dallas', 'United States'),
            'us-west1': (1, 'Oregon', 'United States'),
            'us-west2': (2, 'Los Angeles', 'United States'),
            'us-west3': (2, 'Salt Lake City', 'United States'),
            'us-west4': (2, 'Las Vegas', 'United States')
        }

    def tier1(self) -> List[str]:
        # Return a list of tier 1 GCP regions
        return [region for region, info in self.regions.items() if info[0] == 1]

    def tier2(self) -> List[str]:
        # Return a list of tier 2 GCP regions
        return [region for region, info in self.regions.items() if info[0] == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        # Ping a GCP region and return latency statistics
        ping_cmd = ['ping', '-c', str(attempts), f'{region}.gcp.cloudping.com']
        if platform.system().lower() == 'windows':
            ping_cmd = ['ping', '-n',
                        str(attempts), f'{region}.gcp.cloudping.com']

        try:
            output = subprocess.check_output(
                ping_cmd).decode('utf-8').split('\n')
            times = []
            for line in output:
                if 'time=' in line:
                    time = float(line.split('time=')[1].split('ms')[0])
                    times.append(time)

            if times:
                mean_latency = statistics.mean(times)
                std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
                min_latency = min(times)
                max_latency = max(times)
                return region, mean_latency, std_dev, min_latency, max_latency
            else:
                return region, float('inf'), float('inf'), float('inf'), float('inf')
        except Exception as e:
            print(f'Error pinging {region}: {e}')
            return region, float('inf'), float('inf'), float('inf'), float('inf')

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
        # Filter regions by tier if specified
        if tier is not None:
            regions_to_test = [region for region,
                               info in self.regions.items() if info[0] == tier]
        else:
            regions_to_test = list(self.regions.keys())

        # Ping each region and store latency statistics
        latency_results = []
        for region in regions_to_test:
            result = self._ping_region(region, attempts)
            latency_results.append(result)

        # Sort latency results by mean latency
        latency_results.sort(key=lambda x: x[1])

        # Print detailed latency information if verbose
        if verbose:
            for region, mean_latency, std_dev, min_latency, max_latency in latency_results:
                print(f'Region: {region}, Mean Latency: {mean_latency:.2f} ms, Std Dev: {std_dev:.2f} ms, '
                      f'Min Latency: {min_latency:.2f} ms, Max Latency: {max_latency:.2f} ms')

        # Return top N regions with lowest latency
        return latency_results[:top]

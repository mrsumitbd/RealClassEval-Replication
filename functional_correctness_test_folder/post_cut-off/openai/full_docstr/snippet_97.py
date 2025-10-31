
import subprocess
import platform
import re
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
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # Tier 1 regions
            'us-central1': (1, 'Iowa', 'USA'),
            'us-east1': (1, 'South Carolina', 'USA'),
            'us-west1': (1, 'Oregon', 'USA'),
            'europe-west1': (1, 'Belgium', 'EU'),
            'asia-east1': (1, 'Taiwan', 'Asia'),
            'asia-northeast1': (1, 'Tokyo', 'Asia'),
            'asia-south1': (1, 'Mumbai', 'Asia'),
            'australia-southeast1': (1, 'Sydney', 'Australia'),
            # Tier 2 regions
            'us-east4': (2, 'Virginia', 'USA'),
            'us-west2': (2, 'Los Angeles', 'USA'),
            'europe-west2': (2, 'London', 'UK'),
            'europe-west3': (2, 'Frankfurt', 'Germany'),
            'asia-southeast1': (2, 'Singapore', 'Asia'),
            'asia-southeast2': (2, 'Jakarta', 'Asia'),
            'australia-southeast2': (2, 'Melbourne', 'Australia'),
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
        is_windows = platform.system().lower() == 'windows'
        cmd = ['ping', '-n' if is_windows else '-c', str(attempts), region]
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )
            output = result.stdout
            if is_windows:
                # Windows ping summary: Minimum = Xms, Maximum = Xms, Average = Xms
                m = re.search(
                    r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', output)
                if m:
                    min_lat = float(m.group(1))
                    max_lat = float(m.group(2))
                    mean_lat = float(m.group(3))
                    std_lat = 0.0  # Windows ping does not provide std dev
                    return region, mean_lat, std_lat, min_lat, max_lat
            else:
                # Unix ping summary: rtt min/avg/max/mdev = X/X/X/X ms
                m = re.search(
                    r'rtt min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms', output)
                if m:
                    min_lat = float(m.group(1))
                    mean_lat = float(m.group(2))
                    max_lat = float(m.group(3))
                    std_lat = float(m.group(4))
                    return region, mean_lat, std_lat, min_lat, max_lat
            # If parsing fails, fallback to high latency
            return region, float('inf'), 0.0, float('inf'), float('inf')
        except Exception:
            return region, float('inf'), 0.0, float('inf'), float('inf')

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
            attempts (int): Number of

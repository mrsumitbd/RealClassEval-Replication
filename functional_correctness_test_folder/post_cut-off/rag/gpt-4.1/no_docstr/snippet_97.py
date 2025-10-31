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
        '''Initializes the GCPRegions class with predefined Google Cloud Platform regions and their details.'''
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # region: (tier, city, country)
            "us-central1": (1, "Iowa", "USA"),
            "us-east1": (1, "South Carolina", "USA"),
            "us-east4": (1, "Northern Virginia", "USA"),
            "us-west1": (1, "Oregon", "USA"),
            "us-west2": (2, "Los Angeles", "USA"),
            "us-west3": (2, "Salt Lake City", "USA"),
            "us-west4": (2, "Las Vegas", "USA"),
            "northamerica-northeast1": (2, "Montreal", "Canada"),
            "northamerica-northeast2": (2, "Toronto", "Canada"),
            "southamerica-east1": (2, "Sao Paulo", "Brazil"),
            "southamerica-west1": (2, "Santiago", "Chile"),
            "europe-west1": (1, "Belgium", "Europe"),
            "europe-west2": (1, "London", "UK"),
            "europe-west3": (1, "Frankfurt", "Germany"),
            "europe-west4": (1, "Netherlands", "Europe"),
            "europe-west6": (2, "Zurich", "Switzerland"),
            "europe-central2": (2, "Warsaw", "Poland"),
            "europe-north1": (2, "Finland", "Europe"),
            "europe-southwest1": (2, "Madrid", "Spain"),
            "europe-west8": (2, "Milan", "Italy"),
            "europe-west9": (2, "Paris", "France"),
            "asia-east1": (1, "Taiwan", "Asia"),
            "asia-east2": (2, "Hong Kong", "Asia"),
            "asia-northeast1": (1, "Tokyo", "Japan"),
            "asia-northeast2": (2, "Osaka", "Japan"),
            "asia-northeast3": (2, "Seoul", "South Korea"),
            "asia-south1": (2, "Mumbai", "India"),
            "asia-south2": (2, "Delhi", "India"),
            "asia-southeast1": (1, "Singapore", "Asia"),
            "asia-southeast2": (2, "Jakarta", "Indonesia"),
            "australia-southeast1": (2, "Sydney", "Australia"),
            "australia-southeast2": (2, "Melbourne", "Australia"),
            "me-west1": (2, "Tel Aviv", "Israel"),
            "me-central1": (2, "Doha", "Qatar"),
            "africa-south1": (2, "Johannesburg", "South Africa"),
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
        # GCP region ping test: use the region's public DNS endpoint
        # e.g., region "us-central1" => "us-central1.gcping.com"
        host = f"{region}.gcping.com"
        latencies = []
        for _ in range(attempts):
            try:
                # Use system ping, 1 packet, wait max 2s
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "2", host],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                output = result.stdout
                # Parse time=XX ms
                for line in output.splitlines():
                    if "time=" in line:
                        idx = line.find("time=")
                        ms = line[idx+5:].split(" ")[0]
                        latencies.append(float(ms))
                        break
            except Exception:
                continue
        if latencies:
            mean = statistics.mean(latencies)
            stddev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
            minv = min(latencies)
            maxv = max(latencies)
        else:
            mean = stddev = minv = maxv = float("inf")
        return (region, mean, stddev, minv, maxv)

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
        # Filter out regions with no response (mean == inf)
        results = [r for r in results if r[1] != float("inf")]
        results.sort(key=lambda x: x[1])
        if verbose:
            print("Region latency statistics:")
            for r in results:
                print(
                    f"{r[0]:<25} mean={r[1]:.2f}ms std={r[2]:.2f}ms min={r[3]:.2f}ms max={r[4]:.2f}ms")
        return results[:top]

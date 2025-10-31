from typing import Dict, Tuple, List, Optional
import time
import math
import statistics
import urllib.request
import urllib.error


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
        # Tier is a rough categorization: 1 for primary/established major regions, 2 for others
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # Americas
            "us-central1": (1, "Iowa", "USA"),
            "us-east1": (1, "South Carolina", "USA"),
            "us-east4": (1, "Northern Virginia", "USA"),
            "us-west1": (1, "Oregon", "USA"),
            "us-west2": (2, "Los Angeles", "USA"),
            "us-west3": (2, "Salt Lake City", "USA"),
            "us-west4": (2, "Las Vegas", "USA"),
            "us-south1": (2, "Dallas", "USA"),
            "northamerica-northeast1": (1, "Montréal", "Canada"),
            "northamerica-northeast2": (2, "Toronto", "Canada"),
            "southamerica-east1": (1, "São Paulo", "Brazil"),
            "southamerica-west1": (2, "Santiago", "Chile"),
            # Europe
            "europe-west1": (1, "Belgium", "Belgium"),
            "europe-west2": (1, "London", "UK"),
            "europe-west3": (2, "Frankfurt", "Germany"),
            "europe-west4": (1, "Netherlands", "Netherlands"),
            "europe-west6": (2, "Zurich", "Switzerland"),
            "europe-west8": (2, "Milan", "Italy"),
            "europe-west9": (2, "Paris", "France"),
            "europe-central2": (2, "Warsaw", "Poland"),
            "europe-north1": (2, "Hamina", "Finland"),
            # Middle East
            "me-central1": (2, "Doha", "Qatar"),
            "me-central2": (2, "Dammam", "Saudi Arabia"),
            "me-west1": (2, "Tel Aviv", "Israel"),
            # Asia
            "asia-east1": (1, "Taiwan", "Taiwan"),
            "asia-east2": (2, "Hong Kong", "China"),
            "asia-northeast1": (1, "Tokyo", "Japan"),
            "asia-northeast2": (2, "Osaka", "Japan"),
            "asia-northeast3": (2, "Seoul", "South Korea"),
            "asia-south1": (1, "Mumbai", "India"),
            "asia-south2": (2, "Delhi", "India"),
            "asia-southeast1": (1, "Singapore", "Singapore"),
            "asia-southeast2": (2, "Jakarta", "Indonesia"),
            # Oceania
            "australia-southeast1": (1, "Sydney", "Australia"),
            "australia-southeast2": (2, "Melbourne", "Australia"),
        }

    def tier1(self) -> List[str]:
        return [r for r, (t, _, __) in self.regions.items() if t == 1]

    def tier2(self) -> List[str]:
        return [r for r, (t, _, __) in self.regions.items() if t == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        if attempts < 1:
            attempts = 1
        url = f"https://{region}.gcping.com/ping"
        latencies_ms: List[float] = []
        for _ in range(attempts):
            start = time.perf_counter()
            try:
                with urllib.request.urlopen(url, timeout=2.5) as resp:
                    # Read a small amount to ensure request completes
                    _ = resp.read()
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                latencies_ms.append(elapsed_ms)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
                # Skip failed attempt
                continue
        if not latencies_ms:
            return (region, math.inf, math.inf, math.inf, math.inf)
        mean_v = statistics.fmean(latencies_ms)
        std_v = statistics.pstdev(latencies_ms) if len(
            latencies_ms) > 1 else 0.0
        min_v = min(latencies_ms)
        max_v = max(latencies_ms)
        return (region, mean_v, std_v, min_v, max_v)

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
        if top < 1:
            top = 1
        if attempts < 1:
            attempts = 1

        if tier is None:
            test_regions = list(self.regions.keys())
        elif tier == 1:
            test_regions = self.tier1()
        elif tier == 2:
            test_regions = self.tier2()
        else:
            raise ValueError("tier must be None, 1, or 2")

        results = [self._ping_region(r, attempts=attempts)
                   for r in test_regions]
        # sort by mean latency, then min latency
        results.sort(key=lambda x: (x[1], x[3]))

        if verbose:
            for region, mean_v, std_v, min_v, max_v in results:
                if math.isinf(mean_v):
                    print(f"{region}: unreachable")
                else:
                    print(
                        f"{region}: mean={mean_v:.1f} ms, std={std_v:.1f} ms, min={min_v:.1f} ms, max={max_v:.1f} ms")

        # Filter out unreachable (mean == inf)
        reachable = [r for r in results if not math.isinf(r[1])]
        return reachable[:top] if reachable else results[:top]

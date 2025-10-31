from typing import List, Tuple, Optional, Dict
import time
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
        '''Initializes the GCPRegions class with predefined Google Cloud Platform regions and their details.'''
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # Americas
            "us-central1": (1, "Iowa", "USA"),
            "us-east1": (1, "South Carolina", "USA"),
            "us-east4": (1, "Northern Virginia", "USA"),
            "us-west1": (1, "Oregon", "USA"),
            "us-west2": (2, "Los Angeles, California", "USA"),
            "us-west3": (2, "Salt Lake City, Utah", "USA"),
            "us-west4": (2, "Las Vegas, Nevada", "USA"),
            "northamerica-northeast1": (2, "Montreal, Quebec", "Canada"),
            "northamerica-northeast2": (2, "Toronto, Ontario", "Canada"),
            "southamerica-east1": (2, "São Paulo", "Brazil"),
            "southamerica-west1": (2, "Santiago", "Chile"),
            # Europe
            "europe-west1": (1, "St. Ghislain", "Belgium"),
            "europe-west2": (1, "London", "United Kingdom"),
            "europe-west3": (1, "Frankfurt", "Germany"),
            "europe-west4": (1, "Eemshaven", "Netherlands"),
            "europe-west6": (2, "Zurich", "Switzerland"),
            "europe-west8": (2, "Milan", "Italy"),
            "europe-west9": (2, "Paris", "France"),
            "europe-north1": (2, "Hamina", "Finland"),
            "europe-central2": (2, "Warsaw", "Poland"),
            # Asia Pacific
            "asia-east1": (1, "Changhua County", "Taiwan"),
            "asia-east2": (2, "Hong Kong", "China"),
            "asia-northeast1": (1, "Tokyo", "Japan"),
            "asia-northeast2": (2, "Osaka", "Japan"),
            "asia-northeast3": (2, "Seoul", "South Korea"),
            "asia-south1": (2, "Mumbai", "India"),
            "asia-south2": (2, "Delhi", "India"),
            "asia-southeast1": (1, "Jurong West", "Singapore"),
            "asia-southeast2": (2, "Jakarta", "Indonesia"),
            # Australia
            "australia-southeast1": (1, "Sydney", "Australia"),
            "australia-southeast2": (2, "Melbourne", "Australia"),
            # Middle East and Africa
            "me-central1": (2, "Doha", "Qatar"),
            "me-west1": (2, "Tel Aviv", "Israel"),
            "africa-south1": (2, "Johannesburg", "South Africa"),
        }

    def tier1(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 1 based on predefined criteria.'''
        return [r for r, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 2 based on predefined criteria.'''
        return [r for r, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        '''Pings a specified GCP region and returns latency statistics: mean, min, max, and standard deviation.'''
        # Use HTTP ping via gcping endpoints to estimate latency to region
        url = f"https://{region}.gcping.com/ping"
        samples: List[float] = []
        for _ in range(max(1, attempts)):
            t0 = time.perf_counter()
            try:
                with urllib.request.urlopen(url, timeout=3) as resp:
                    # read a small amount to ensure response is received
                    resp.read(1)
                dt_ms = (time.perf_counter() - t0) * 1000.0
                samples.append(dt_ms)
            except Exception:
                samples.append(float("inf"))

        finite = [s for s in samples if s != float("inf")]
        if not finite:
            return (region, float("inf"), float("inf"), float("inf"), float("inf"))

        mean = sum(finite) / len(finite)
        mn = min(finite)
        mx = max(finite)
        std = statistics.stdev(finite) if len(finite) > 1 else 0.0
        return (region, mean, std, mn, mx)

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
            attempts (int): Number of ping attempts per region.
        Returns:
            (List[Tuple[str, float, float, float, float]]): List of tuples containing region information and
            latency statistics. Each tuple contains (region, mean_latency, std_dev, min_latency, max_latency).
        Examples:
            >>> regions = GCPRegions()
            >>> results = regions.lowest_latency(top=3, verbose=True, tier=1, attempts=2)
            >>> print(results[0][0])  # Print the name of the lowest latency region
        '''
        if tier is None:
            region_list = list(self.regions.keys())
        elif tier == 1:
            region_list = self.tier1()
        elif tier == 2:
            region_list = self.tier2()
        else:
            raise ValueError("tier must be 1, 2, or None")

        results = [self._ping_region(r, attempts=attempts)
                   for r in region_list]
        # Sort by mean latency then by min latency as tie-breaker
        results.sort(key=lambda x: (x[1], x[3]))

        if verbose:
            for r, mean, std, mn, mx in results:
                mean_s = "inf" if mean == float("inf") else f"{mean:.1f}"
                std_s = "inf" if std == float("inf") else f"{std:.1f}"
                mn_s = "inf" if mn == float("inf") else f"{mn:.1f}"
                mx_s = "inf" if mx == float("inf") else f"{mx:.1f}"
                print(
                    f"{r}: mean={mean_s} ms, std={std_s} ms, min={mn_s} ms, max={mx_s} ms")

        return results[: max(1, top)]

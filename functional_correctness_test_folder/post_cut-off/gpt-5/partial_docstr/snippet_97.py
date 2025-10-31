from typing import Dict, List, Optional, Tuple
import time
import math
import statistics
import requests


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
        # region -> (tier, city, country)
        tier1_regions = {
            "us-central1": ("Council Bluffs", "United States"),
            "us-east1": ("Moncks Corner, SC", "United States"),
            "us-east4": ("Ashburn, VA", "United States"),
            "us-west1": ("The Dalles, OR", "United States"),
            "us-west2": ("Los Angeles, CA", "United States"),
            "us-west3": ("Salt Lake City, UT", "United States"),
            "us-west4": ("Las Vegas, NV", "United States"),
            "us-south1": ("Dallas, TX", "United States"),
            "northamerica-northeast1": ("Montreal", "Canada"),
            "europe-west1": ("St. Ghislain", "Belgium"),
            "europe-west2": ("London", "United Kingdom"),
            "europe-west3": ("Frankfurt", "Germany"),
            "europe-west4": ("Eemshaven", "Netherlands"),
            "europe-west6": ("Zurich", "Switzerland"),
            "europe-north1": ("Hamina", "Finland"),
            "asia-east1": ("Changhua County", "Taiwan"),
            "asia-northeast1": ("Tokyo", "Japan"),
            "asia-southeast1": ("Jurong West", "Singapore"),
            "australia-southeast1": ("Sydney", "Australia"),
            "southamerica-east1": ("São Paulo", "Brazil"),
        }
        other_regions = {
            "asia-east2": ("Hong Kong", "Hong Kong"),
            "asia-northeast2": ("Osaka", "Japan"),
            "asia-northeast3": ("Seoul", "South Korea"),
            "asia-south1": ("Mumbai", "India"),
            "asia-south2": ("Delhi", "India"),
            "asia-southeast2": ("Jakarta", "Indonesia"),
            "australia-southeast2": ("Melbourne", "Australia"),
            "europe-central2": ("Warsaw", "Poland"),
            "europe-west8": ("Milan", "Italy"),
            "europe-west9": ("Paris", "France"),
            "europe-southwest1": ("Madrid", "Spain"),
            "me-central1": ("Doha", "Qatar"),
            "me-west1": ("Tel Aviv", "Israel"),
            "northamerica-northeast2": ("Toronto", "Canada"),
            "southamerica-west1": ("Santiago", "Chile"),
            "us-east5": ("Columbus, OH", "United States"),
        }

        self.regions: Dict[str, Tuple[int, str, str]] = {}
        for r, (city, country) in tier1_regions.items():
            self.regions[r] = (1, city, country)
        for r, (city, country) in other_regions.items():
            self.regions[r] = (2, city, country)

    def tier1(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 1 based on predefined criteria.'''
        return [r for r, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 2 based on predefined criteria.'''
        return [r for r, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        '''Pings a specified GCP region and returns latency statistics: mean, min, max, and standard deviation.'''
        url = f"https://gcping.com/api/latency?target={region}"
        latencies: List[float] = []
        for _ in range(max(1, attempts)):
            start = time.perf_counter()
            try:
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                val = resp.json()
                # gcping returns value in ms, ensure float
                latency_ms = float(val) if not isinstance(
                    val, dict) else float(val.get("latency", math.nan))
            except Exception:
                latency_ms = math.inf
            finally:
                _ = time.perf_counter() - start
            if math.isfinite(latency_ms):
                latencies.append(latency_ms)

        if not latencies:
            mean = math.inf
            std = math.nan
            min_v = math.inf
            max_v = math.inf
        else:
            mean = float(sum(latencies) / len(latencies))
            min_v = float(min(latencies))
            max_v = float(max(latencies))
            std = float(statistics.pstdev(latencies)) if len(
                latencies) > 1 else 0.0

        return region, mean, std, min_v, max_v

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
        if tier is not None and tier not in (1, 2):
            raise ValueError("tier must be 1, 2, or None")

        candidate_regions = [
            r for r, (t, _, _) in self.regions.items() if tier is None or t == tier]
        results: List[Tuple[str, float, float, float, float]] = []

        for r in candidate_regions:
            stats = self._ping_region(r, attempts=attempts)
            results.append(stats)

        if verbose:
            for r, mean, std, mn, mx in results:
                tier_info = self.regions.get(r, (None, "", ""))[0]
                print(
                    f"{r} (tier {tier_info}): mean={mean:.2f}ms, std={0.0 if math.isnan(std) else std:.2f}ms, min={mn:.2f}ms, max={mx:.2f}ms")

        finite_results = [x for x in results if math.isfinite(x[1])]
        if not finite_results:
            return []

        finite_results.sort(key=lambda x: (x[1], x[2]))
        return finite_results[: max(1, top)]

from typing import Dict, Tuple, List, Optional
import time
import statistics
import math
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
        # tier: 1 (core/common), 2 (other/extended)
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # North America
            "us-central1": (1, "Council Bluffs", "USA"),
            "us-east1": (1, "Moncks Corner", "USA"),
            "us-east4": (1, "Ashburn", "USA"),
            "us-west1": (1, "The Dalles", "USA"),
            "us-west2": (2, "Los Angeles", "USA"),
            "us-west3": (2, "Salt Lake City", "USA"),
            "us-west4": (2, "Las Vegas", "USA"),
            "northamerica-northeast1": (2, "Montréal", "Canada"),
            "northamerica-northeast2": (2, "Toronto", "Canada"),
            "southamerica-east1": (2, "São Paulo", "Brazil"),
            "southamerica-west1": (2, "Santiago", "Chile"),
            # Europe
            "europe-west1": (1, "St. Ghislain (Mons)", "Belgium"),
            "europe-west2": (2, "London", "United Kingdom"),
            "europe-west3": (1, "Frankfurt", "Germany"),
            "europe-west4": (1, "Eemshaven", "Netherlands"),
            "europe-west6": (2, "Zürich", "Switzerland"),
            "europe-west8": (2, "Milan", "Italy"),
            "europe-west9": (2, "Paris", "France"),
            "europe-central2": (2, "Warsaw", "Poland"),
            "europe-southwest1": (2, "Madrid", "Spain"),
            # Asia
            "asia-east1": (1, "Changhua County", "Taiwan"),
            "asia-east2": (2, "Hong Kong", "China (Hong Kong)"),
            "asia-northeast1": (1, "Tokyo", "Japan"),
            "asia-northeast2": (2, "Osaka", "Japan"),
            "asia-northeast3": (2, "Seoul", "South Korea"),
            "asia-southeast1": (1, "Singapore", "Singapore"),
            "asia-southeast2": (2, "Jakarta", "Indonesia"),
            "asia-south1": (2, "Mumbai", "India"),
            "asia-south2": (2, "Delhi (NCR)", "India"),
            # Oceania
            "australia-southeast1": (1, "Sydney", "Australia"),
            "australia-southeast2": (2, "Melbourne", "Australia"),
            # Middle East and Africa
            "me-west1": (2, "Tel Aviv", "Israel"),
            "me-central1": (2, "Doha", "Qatar"),
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
        # Use gcping endpoints to estimate latency via HTTPS requests
        # Endpoint example: https://us-central1.gcping.com/
        url = f"https://{region}.gcping.com/"
        times_ms: List[float] = []

        for _ in range(max(1, attempts)):
            start = time.perf_counter()
            try:
                # Use HEAD to minimize payload; small timeout to avoid long stalls
                resp = requests.head(url, timeout=2.5)
                # Some endpoints may not support HEAD; fallback to GET if needed
                if resp.status_code >= 400:
                    resp = requests.get(url, timeout=2.5)
                if 200 <= resp.status_code < 400:
                    elapsed_ms = (time.perf_counter() - start) * 1000.0
                    times_ms.append(elapsed_ms)
                else:
                    # Treat non-success as failed attempt
                    pass
            except Exception:
                # Ignore failures for this attempt
                pass

        if not times_ms:
            return (region, math.inf, math.inf, math.inf, math.inf)

        mean = statistics.fmean(times_ms)
        mn = min(times_ms)
        mx = max(times_ms)
        std = statistics.pstdev(times_ms) if len(times_ms) > 1 else 0.0
        return (region, mean, std, mn, mx)

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
        if tier not in (None, 1, 2):
            raise ValueError("tier must be None, 1, or 2")

        candidates = self.regions.keys() if tier is None else (
            self.tier1() if tier == 1 else self.tier2())
        results: List[Tuple[str, float, float, float, float]] = []

        for region in candidates:
            stats = self._ping_region(region, attempts=attempts)
            results.append(stats)

        # Optionally display all results
        if verbose:
            print("Region latency results (mean ms, std ms, min ms, max ms):")
            for r, mean, std, mn, mx in sorted(results, key=lambda x: x[1]):
                city, country = self.regions.get(r, (None, "", ""))[1:]
                if math.isinf(mean):
                    print(
                        f"- {r:<25} {'N/A':>8}   {'N/A':>8}   {'N/A':>8}   {'N/A':>8}  {city}, {country}")
                else:
                    print(
                        f"- {r:<25} {mean:8.1f}   {std:8.1f}   {mn:8.1f}   {mx:8.1f}  {city}, {country}")

        # Filter out failed regions (inf mean) before sorting and slicing
        filtered = [t for t in results if not math.isinf(t[1])]
        filtered.sort(key=lambda x: x[1])

        return filtered[: max(1, top)] if filtered else []

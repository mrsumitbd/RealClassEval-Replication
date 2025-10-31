from typing import Dict, List, Tuple, Optional
import time
import statistics
import urllib.request
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
        >>> regions = GCPRegions()
        >>> lowest_latency_region = regions.lowest_latency(verbose=True, attempts=3)
        >>> print(f"Lowest latency region: {lowest_latency_region[0][0]}")
    '''

    def __init__(self):
        '''Initializes the GCPRegions class with predefined Google Cloud Platform regions and their details.'''
        t1 = {
            "us-central1": ("Iowa", "USA"),
            "us-east1": ("South Carolina", "USA"),
            "us-west1": ("Oregon", "USA"),
            "europe-west1": ("Belgium", "Belgium"),
            "asia-east1": ("Taiwan", "Taiwan"),
            "asia-northeast1": ("Tokyo", "Japan"),
            "europe-west4": ("Netherlands", "Netherlands"),
        }
        t2 = {
            "us-east4": ("Northern Virginia", "USA"),
            "us-west2": ("Los Angeles", "USA"),
            "us-west3": ("Salt Lake City", "USA"),
            "us-west4": ("Las Vegas", "USA"),
            "northamerica-northeast1": ("Montreal", "Canada"),
            "northamerica-northeast2": ("Toronto", "Canada"),
            "southamerica-east1": ("São Paulo", "Brazil"),
            "southamerica-west1": ("Santiago", "Chile"),
            "europe-north1": ("Hamina", "Finland"),
            "europe-central2": ("Warsaw", "Poland"),
            "europe-west2": ("London", "UK"),
            "europe-west3": ("Frankfurt", "Germany"),
            "europe-west6": ("Zurich", "Switzerland"),
            "europe-west8": ("Milan", "Italy"),
            "europe-west9": ("Paris", "France"),
            "asia-east2": ("Hong Kong", "China"),
            "asia-northeast2": ("Osaka", "Japan"),
            "asia-northeast3": ("Seoul", "South Korea"),
            "asia-south1": ("Mumbai", "India"),
            "asia-south2": ("Delhi", "India"),
            "asia-southeast1": ("Singapore", "Singapore"),
            "asia-southeast2": ("Jakarta", "Indonesia"),
            "australia-southeast1": ("Sydney", "Australia"),
            "australia-southeast2": ("Melbourne", "Australia"),
        }
        self.regions: Dict[str, Tuple[int, str, str]] = {}
        for r, (city, country) in t1.items():
            self.regions[r] = (1, city, country)
        for r, (city, country) in t2.items():
            self.regions[r] = (2, city, country)

    def tier1(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 1 based on predefined criteria.'''
        return sorted([r for r, (tier, _, _) in self.regions.items() if tier == 1])

    def tier2(self) -> List[str]:
        '''Returns a list of GCP regions classified as tier 2 based on predefined criteria.'''
        return sorted([r for r, (tier, _, _) in self.regions.items() if tier == 2])

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        '''Pings a specified GCP region and returns latency statistics: mean, min, max, and standard deviation.'''
        # Use gcping regional endpoints via HTTPS.
        # Measure client-observed round-trip latency using time.monotonic.
        url = f"https://{region}.gcping.com/ping"
        samples: List[float] = []
        for _ in range(max(1, attempts)):
            t0 = time.monotonic()
            try:
                with urllib.request.urlopen(url, timeout=3) as _resp:
                    pass
                dt_ms = (time.monotonic() - t0) * 1000.0
                samples.append(dt_ms)
            except Exception:
                # On failure, record an infinite latency for this attempt
                samples.append(float("inf"))

        # Filter out infinities if there are any successful samples
        finite = [x for x in samples if math.isfinite(x)]
        if not finite:
            mean = float("inf")
            mn = float("inf")
            mx = float("inf")
            sd = float("inf")
        else:
            mean = statistics.fmean(finite)
            mn = min(finite)
            mx = max(finite)
            sd = statistics.pstdev(finite) if len(finite) > 1 else 0.0

        return (region, mean, sd, mn, mx)

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
        if tier not in (None, 1, 2):
            raise ValueError("tier must be None, 1, or 2")

        if tier == 1:
            candidates = self.tier1()
        elif tier == 2:
            candidates = self.tier2()
        else:
            candidates = sorted(self.regions.keys())

        results: List[Tuple[str, float, float, float, float]] = []
        for r in candidates:
            stats = self._ping_region(r, attempts=attempts)
            results.append(stats)

        # Sort by mean latency, placing inf at the end
        results.sort(key=lambda x: (math.isinf(x[1]), x[1]))

        if verbose:
            for r, mean, sd, mn, mx in results:
                tier_val, city, country = self.regions.get(r, (0, "", ""))
                if math.isinf(mean):
                    print(f"{r:25s} - no response")
                else:
                    print(
                        f"{r:25s} {mean:.1f} ms ± {sd:.1f} (min {mn:.1f}, max {mx:.1f}) - Tier {tier_val} - {city}, {country}"
                    )

        return results[: max(1, top)]

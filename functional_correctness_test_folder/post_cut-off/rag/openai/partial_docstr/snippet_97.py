
import subprocess
import statistics
import re
from typing import Dict, List, Optional, Tuple


class GCPRegions:
    """
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
    """

    def __init__(self):
        """Initializes the GCPRegions class with predefined Google Cloud Platform regions and their details."""
        # The tuple format is (tier, city, country)
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # Tier 1 regions
            "us-central1": (1, "Iowa", "USA"),
            "us-east1": (1, "South Carolina", "USA"),
            "us-east4": (1, "Northern Virginia", "USA"),
            "us-west1": (1, "Oregon", "USA"),
            "us-west2": (1, "Los Angeles", "USA"),
            "europe-west1": (1, "Belgium", "Belgium"),
            "europe-west2": (1, "London", "UK"),
            "asia-east1": (1, "Taiwan", "Taiwan"),
            "asia-northeast1": (1, "Tokyo", "Japan"),
            "asia-southeast1": (1, "Singapore", "Singapore"),
            "australia-southeast1": (1, "Sydney", "Australia"),
            "southamerica-east1": (1, "São Paulo", "Brazil"),
            # Tier 2 regions
            "us-east5": (2, "Virginia", "USA"),
            "us-west3": (2, "San Francisco", "USA"),
            "europe-west3": (2, "Frankfurt", "Germany"),
            "europe-west4": (2, "Netherlands", "Netherlands"),
            "asia-south1": (2, "Mumbai", "India"),
            "asia-south2": (2, "Delhi", "India"),
            "asia-northeast2": (2, "Osaka", "Japan"),
            "asia-northeast3": (2, "Seoul", "South Korea"),
            "asia-east2": (2, "Hong Kong", "Hong Kong"),
            "asia-southeast2": (2, "Jakarta", "Indonesia"),
            "australia-southeast2": (2, "Melbourne", "Australia"),
            "southamerica-west1": (2, "Santiago", "Chile"),
        }

    def tier1(self) -> List[str]:
        """Returns a list of GCP regions classified as tier 1 based on predefined criteria."""
        return [region for region, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        """Returns a list of GCP regions classified as tier 2 based on predefined criteria."""
        return [region for region, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        """
        Pings a specified GCP region and returns latency statistics: mean, min, max, and standard deviation.
        Returns a tuple: (region, mean, std_dev, min, max)
        """
        # Resolve the region to a DNS name that can be pinged
        # Using the compute.googleapis.com endpoint for the region
        host = f"{region}.compute.googleapis.com"

        # Build the ping command
        cmd = ["ping", "-c", str(attempts), host]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=attempts * 5,
            )
            output = result.stdout
        except Exception:
            # If ping fails, return infinities
            return (region, float("inf"), float("inf"), float("inf"), float("inf"))

        # Extract time= values from the output
        times = []
        for line in output.splitlines():
            match = re.search(r"time=([\d\.]+) ms", line)
            if match:
                times.append(float(match.group(1)))

        if not times:
            # No successful pings
            return (region, float("inf"), float("inf"), float("inf"), float("inf"))

        mean = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
        min_latency = min(times)
        max_latency = max(times)
        return (region, mean, std_dev, min_latency, max_latency)

    def lowest_latency(
        self,
        top: int = 1,
        verbose: bool = False,
        tier: Optional[int] = None,
        attempts: int = 1,
    ) -> List[Tuple[str, float, float, float, float]]:
        """
        Determines the GCP regions with the lowest latency based on ping tests.
        Args:
            top (int): Number of top regions to return.
            verbose (bool): If True, prints detailed latency information for all tested regions.
            tier (int | None): Filter regions by tier (1 or 2). If None, all regions are tested.
            attempts (int): Number of ping attempts per region.
        Returns:
            (List[Tuple[str, float, float, float, float]]): List of tuples containing region information and
            latency statistics. Each tuple contains (region, mean_latency

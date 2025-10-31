
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

    def __init__(self):
        self.regions: Dict[str, Tuple[int, str, str]] = {
            # Tier 1
            "us-central1": (1, "Council Bluffs", "USA"),
            "us-east1": (1, "Moncks Corner", "USA"),
            "us-east4": (1, "Ashburn", "USA"),
            "us-west1": (1, "The Dalles", "USA"),
            "europe-west1": (1, "St. Ghislain", "Belgium"),
            "europe-west4": (1, "Eemshaven", "Netherlands"),
            "asia-east1": (1, "Changhua County", "Taiwan"),
            "asia-northeast1": (1, "Tokyo", "Japan"),
            # Tier 2
            "us-west2": (2, "Los Angeles", "USA"),
            "us-west3": (2, "Salt Lake City", "USA"),
            "us-west4": (2, "Las Vegas", "USA"),
            "us-east5": (2, "Columbus", "USA"),
            "northamerica-northeast1": (2, "Montréal", "Canada"),
            "southamerica-east1": (2, "São Paulo", "Brazil"),
            "europe-north1": (2, "Hamina", "Finland"),
            "europe-west2": (2, "London", "UK"),
            "europe-west3": (2, "Frankfurt", "Germany"),
            "europe-west6": (2, "Zürich", "Switzerland"),
            "asia-south1": (2, "Mumbai", "India"),
            "asia-southeast1": (2, "Jurong West", "Singapore"),
            "asia-northeast2": (2, "Osaka", "Japan"),
            "asia-northeast3": (2, "Seoul", "South Korea"),
            "australia-southeast1": (2, "Sydney", "Australia"),
            "australia-southeast2": (2, "Melbourne", "Australia"),
            "asia-south2": (2, "Delhi", "India"),
            "asia-southeast2": (2, "Jakarta", "Indonesia"),
            "europe-central2": (2, "Warsaw", "Poland"),
            "me-west1": (2, "Tel Aviv", "Israel"),
            "me-central1": (2, "Doha", "Qatar"),
            "southamerica-west1": (2, "Santiago", "Chile"),
            "africa-south1": (2, "Johannesburg", "South Africa"),
        }

    def tier1(self) -> List[str]:
        return [region for region, (tier, _, _) in self.regions.items() if tier == 1]

    def tier2(self) -> List[str]:
        return [region for region, (tier, _, _) in self.regions.items() if tier == 2]

    @staticmethod
    def _ping_region(region: str, attempts: int = 1) -> Tuple[str, float, float, float, float]:
        # GCP region FQDN for ping: <region>.gcp.gcping.com
        host = f"{region}.gcp.gcping.com"
        latencies = []
        system = platform.system().lower()
        for _ in range(attempts):
            try:
                if system == "windows":
                    # Windows: ping -n 1 -w 1000 host
                    cmd = ["ping", "-n", "1", "-w", "1000", host]
                else:
                    # Linux/Mac: ping -c 1 -W 1 host
                    cmd = ["ping", "-c", "1", "-W", "1", host]
                proc = subprocess.run(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = proc.stdout
                # Parse latency from output
                latency = None
                if system == "windows":
                    # Look for "Average = XXms"
                    for line in output.splitlines():
                        if "Average =" in line:
                            latency = float(line.split(
                                "Average =")[-1].replace("ms", "").strip())
                            break
                else:
                    # Look for "time=XX ms"
                    for line in output.splitlines():
                        if "time=" in line:
                            idx = line.find("time=")
                            if idx != -1:
                                time_str = line[idx+5:].split(" ")[0]
                                latency = float(time_str)
                                break
                if latency is not None:
                    latencies.append(latency)
            except Exception:
                continue
        if latencies:
            mean = statistics.mean(latencies)
            std = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
            min_latency = min(latencies)
            max_latency = max(latencies)
        else:
            mean = std = min_latency = max_latency = float('inf')
        return (region, mean, std, min_latency, max_latency)

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
        # Sort by mean latency (lowest first)
        results.sort(key=lambda x: x[1])
        if verbose:
            print("Region\t\tMean(ms)\tStd(ms)\t\tMin(ms)\t\tMax(ms)")
            for r in results:
                print(
                    f"{r[0]:<18}{r[1]:<12.2f}{r[2]:<12.2f}{r[3]:<12.2f}{r[4]:<12.2f}")
        return results[:top]

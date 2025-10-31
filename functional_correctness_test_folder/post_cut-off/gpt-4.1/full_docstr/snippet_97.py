
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
        '''Initializes the GCPRegions class with predefined Google Cloud Platform regions and their details.'''
        # region: (tier, city, country)
        self.regions: Dict[str, Tuple[int, str, str]] = {
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
            "europe-west1": (1, "St. Ghislain", "Belgium"),
            "europe-west2": (1, "London", "UK"),
            "europe-west3": (2, "Frankfurt", "Germany"),
            "europe-west4": (2, "Eemshaven", "Netherlands"),
            "europe-west6": (2, "Zürich", "Switzerland"),
            "europe-central2": (2, "Warsaw", "Poland"),
            "europe-north1": (2, "Hamina", "Finland"),
            "asia-east1": (1, "Changhua County", "Taiwan"),
            "asia-east2": (2, "Hong Kong", "Hong Kong"),
            "asia-northeast1": (1, "Tokyo", "Japan"),
            "asia-northeast2": (2, "Osaka", "Japan"),
            "asia-northeast3": (2, "Seoul", "South Korea"),
            "asia-south1": (2, "Mumbai", "India"),
            "asia-south2": (2, "Delhi", "India"),
            "asia-southeast1": (2, "Jurong West", "Singapore"),
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
        # GCP region FQDN for ping: <region>.googleapis.com
        host = f"{region}.googleapis.com"
        plat = platform.system().lower()
        if plat == "windows":
            # Windows: ping -n <count> <host>
            cmd = ["ping", "-n", str(attempts), host]
        else:
            # Linux/Mac: ping -c <count> <host>
            cmd = ["ping", "-c", str(attempts), host]
        try:
            proc = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, text=True)
            output = proc.stdout
            # Parse output for latency times
            times = []
            for line in output.splitlines():
                if plat == "windows":
                    if "time=" in line:
                        # Example: Reply from 142.250.4.10: bytes=32 time=12ms TTL=117
                        idx = line.find("time=")
                        if idx != -1:
                            ms_part = line[idx+5:]
                            ms = ""
                            for c in ms_part:
                                if c.isdigit() or c == ".":
                                    ms += c
                                else:
                                    break
                            if ms:
                                times.append(float(ms))
                else:
                    if "time=" in line:
                        # Example: 64 bytes from 142.250.4.10: icmp_seq=1 ttl=117 time=12.3 ms
                        idx = line.find("time=")
                        if idx != -1:
                            ms_part = line[idx+5:]
                            ms = ""
                            for c in ms_part:
                                if c.isdigit() or c == ".":
                                    ms += c
                                else:
                                    break
                            if ms:
                                times.append(float(ms))
            if not times:
                # If no times found, set to inf
                return (region, float('inf'), float('inf'), float('inf'), float('inf'))
            mean = statistics.mean(times)
            stdev = statistics.stdev(times) if len(times) > 1 else 0.0
            minv = min(times)
            maxv = max(times)
            return (region, mean, stdev, minv, maxv)
        except Exception:
            return (region, float('inf'), float('inf'), float('inf'), float('inf'))

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
        # Sort by mean latency
        results.sort(key=lambda x: x[1])
        if verbose:
            print("Region\t\tMean(ms)\tStd(ms)\tMin(ms)\tMax(ms)")
            for r in results:
                print(
                    f"{r[0]:<20} {r[1]:<10.2f} {r[2]:<8.2f} {r[3]:<8.2f} {r[4]:<8.2f}")
        return results[:top]

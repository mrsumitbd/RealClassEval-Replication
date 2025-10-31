
import json
import os
import time
from typing import Any, Dict, Optional


class DataManager:
    '''Manages data fetching and caching for monitoring.'''

    def __init__(
        self,
        cache_ttl: int = 30,
        hours_back: int = 192,
        data_path: Optional[str] = None,
    ) -> None:
        '''Initialize data manager with cache and fetch settings.
        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory
        '''
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = data_path or os.getcwd()

        # Internal cache state
        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_timestamp: Optional[float] = None
        self._last_error: Optional[str] = None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        '''Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        '''
        if not force_refresh and self._is_cache_valid():
            return self._cache_data

        try:
            # Attempt to load data from a JSON file in the data directory
            file_path = os.path.join(self.data_path, "monitoring_data.json")
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Data file not found: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Optionally trim data to requested hours_back
            if isinstance(data, dict) and "timestamp" in data:
                # Assume data contains a list of records with timestamps
                cutoff = time.time() - self.hours_back * 3600
                records = data.get("records", [])
                filtered = [r for r in records if r.get(
                    "timestamp", 0) >= cutoff]
                data["records"] = filtered

            self._set_cache(data)
            self._last_error = None
            return data

        except Exception as exc:
            self._last_error = str(exc)
            self.invalidate_cache()
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache_data = None
        self._cache_timestamp = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_data is None or self._cache_timestamp is None:
            return False
        return (time.time() - self._cache_timestamp) <= self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache_data = data
        self._cache_timestamp = time.time()

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        if self._cache_timestamp is None:
            return float("inf")
        return time.time() - self._cache_timestamp

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._cache_timestamp

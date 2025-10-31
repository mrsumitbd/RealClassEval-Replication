
import os
import json
import time
from typing import Optional, Dict, Any


class DataManager:
    '''Manages data fetching and caching for monitoring.'''

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        '''Initialize data manager with cache and fetch settings.
        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory
        '''
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = data_path

        # Internal cache state
        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_timestamp: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

        # Ensure data path exists if provided
        if self.data_path and not os.path.isdir(self.data_path):
            os.makedirs(self.data_path, exist_ok=True)

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        '''Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        '''
        # Return cached data if valid and not forced
        if not force_refresh and self._is_cache_valid():
            return self._cache_data

        # Attempt to fetch new data
        try:
            data = self._fetch_data()
            if data is None:
                raise ValueError("Fetched data is None")

            # Update cache and timestamps
            self._set_cache(data)
            self._last_successful_fetch_time = time.time()
            self._last_error = None
            return data
        except Exception as exc:
            self._last_error = str(exc)
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache_data = None
        self._cache_timestamp = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_timestamp is None:
            return False
        return (time.time() - self._cache_timestamp) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Store data in cache with current timestamp.'''
        self._cache_data = data
        self._cache_timestamp = time.time()

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        if self._cache_timestamp is None:
            return 0.0
        return time.time() - self._cache_timestamp

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._last_successful_fetch_time

    # ------------------------------------------------------------------
    # Internal helper methods
    # ------------------------------------------------------------------
    def _fetch_data(self) -> Optional[Dict[str, Any]]:
        '''Simulate data fetching. Reads from a JSON file if available,
        otherwise generates dummy data.'''
        # If a data path is provided, try to read a file named 'data.json'
        if self.data_path:
            data_file = os.path.join(self.data_path, 'data.json')
            if os.path.isfile(data_file):
                try:
                    with open(data_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as exc:
                    raise RuntimeError(
                        f"Failed to read data file: {exc}") from exc

        # No file found or no data_path: generate dummy data
        # Dummy data includes a timestamp and random usage metrics
        dummy = {
            'timestamp': time.time(),
            'usage': {
                'cpu_percent': 42.5,
                'memory_percent': 68.3,
                'disk_percent': 55.1
            },
            'history_hours': self.hours_back
        }
        return dummy

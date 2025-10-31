from typing import Any, Dict, Optional
import time
import os
import json


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
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        '''Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        '''
        if not force_refresh and self._is_cache_valid():
            return self._cache

        try:
            data = self._fetch_data()
            if data is not None:
                self._set_cache(data)
                self._last_error = None
                self._last_successful_fetch_time = time.time()
                return data
            else:
                self._last_error = "Data fetch returned None"
                return None
        except Exception as e:
            self._last_error = str(e)
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache = None
        self._cache_time = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache is None or self._cache_time is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache = data
        self._cache_time = time.time()

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        if self._cache_time is None:
            return float('inf')
        return time.time() - self._cache_time

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._last_successful_fetch_time

    def _fetch_data(self) -> Optional[Dict[str, Any]]:
        '''Fetch data from source (simulate or load from file).'''
        # This is a placeholder for actual data fetching logic.
        # If data_path is set, try to load from a file, else simulate.
        if self.data_path:
            try:
                file_path = os.path.join(
                    self.data_path, "monitoring_data.json")
                with open(file_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                self._last_error = f"Failed to load data from file: {e}"
                return None
        # Simulate data
        now = int(time.time())
        return {
            "timestamp": now,
            "hours_back": self.hours_back,
            "usage": {
                "cpu": 42.0,
                "memory": 73.5,
                "disk": 58.2
            }
        }

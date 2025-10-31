
import time
import os
import json
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
        self._cache = None  # type: Optional[Dict[str, Any]]
        self._cache_time = None  # type: Optional[float]
        self._last_error = None  # type: Optional[str]
        self._last_successful_fetch_time = None  # type: Optional[float]
        self._cache_file = None
        if self.data_path:
            os.makedirs(self.data_path, exist_ok=True)
            self._cache_file = os.path.join(self.data_path, "data_cache.json")
            self._load_cache_from_file()

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
                self._last_successful_fetch_time = self._cache_time
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
        if self._cache_file and os.path.exists(self._cache_file):
            try:
                os.remove(self._cache_file)
            except Exception:
                pass

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache is None or self._cache_time is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache = data
        self._cache_time = time.time()
        if self._cache_file:
            try:
                with open(self._cache_file, "w") as f:
                    json.dump({
                        "cache_time": self._cache_time,
                        "data": self._cache
                    }, f)
            except Exception:
                pass

    def _load_cache_from_file(self):
        if self._cache_file and os.path.exists(self._cache_file):
            try:
                with open(self._cache_file, "r") as f:
                    obj = json.load(f)
                    self._cache_time = obj.get("cache_time")
                    self._cache = obj.get("data")
            except Exception:
                self._cache = None
                self._cache_time = None

    def _fetch_data(self) -> Optional[Dict[str, Any]]:
        # Placeholder for actual data fetching logic.
        # For demonstration, return dummy data.
        # In real use, replace this with actual data fetching.
        # Simulate a fetch delay
        time.sleep(0.1)
        return {
            "timestamp": time.time(),
            "hours_back": self.hours_back,
            "data": [i for i in range(10)]
        }

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

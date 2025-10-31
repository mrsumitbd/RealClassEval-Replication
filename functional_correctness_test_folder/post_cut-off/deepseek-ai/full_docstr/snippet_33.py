
import os
import time
from typing import Optional, Dict, Any
import json
import logging


class DataManager:
    '''Manages data fetching and caching for monitoring.'''

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        '''Initialize data manager with cache and fetch settings.
        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory
        '''
        self._cache_ttl = cache_ttl
        self._hours_back = hours_back
        self._data_path = data_path
        self._cache: Optional[Dict[str, Any]] = None
        self._last_fetch_time: Optional[float] = None
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
            self._set_cache(data)
            self._last_successful_fetch_time = time.time()
            self._last_error = None
            return data
        except Exception as e:
            self._last_error = str(e)
            logging.error(f"Failed to fetch data: {e}")
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache = None
        self._last_fetch_time = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache is None or self._last_fetch_time is None:
            return False
        return (time.time() - self._last_fetch_time) < self._cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache = data
        self._last_fetch_time = time.time()

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        if self._last_fetch_time is None:
            return float('inf')
        return time.time() - self._last_fetch_time

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._last_successful_fetch_time

    def _fetch_data(self) -> Dict[str, Any]:
        '''Fetch data from the source.'''
        # Placeholder for actual data fetching logic
        if self._data_path and os.path.exists(self._data_path):
            with open(self._data_path, 'r') as f:
                return json.load(f)
        else:
            # Simulate fetching data
            return {"data": "sample", "hours_back": self._hours_back}

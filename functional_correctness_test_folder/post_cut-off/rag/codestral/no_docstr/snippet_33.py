
import os
import time
import json
from typing import Dict, Any, Optional


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
        self.data_path = data_path or os.path.join(os.getcwd(), 'data_cache')
        self._cache = None
        self._cache_timestamp = None
        self._last_error = None
        self._last_successful_fetch_time = None

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

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
            # Simulate data fetching (replace with actual data fetching logic)
            data = self._fetch_data()
            self._set_cache(data)
            self._last_successful_fetch_time = time.time()
            self._last_error = None
            return data
        except Exception as e:
            self._last_error = str(e)
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache = None
        self._cache_timestamp = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache is None or self._cache_timestamp is None:
            return False
        return (time.time() - self._cache_timestamp) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache = data
        self._cache_timestamp = time.time()

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        if self._cache_timestamp is None:
            return float('inf')
        return time.time() - self._cache_timestamp

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._last_successful_fetch_time

    def _fetch_data(self) -> Dict[str, Any]:
        '''Simulate data fetching (replace with actual implementation).'''
        # This is a placeholder - replace with actual data fetching logic
        return {
            'timestamp': time.time(),
            'hours_back': self.hours_back,
            'data': {'example': 'data'}
        }

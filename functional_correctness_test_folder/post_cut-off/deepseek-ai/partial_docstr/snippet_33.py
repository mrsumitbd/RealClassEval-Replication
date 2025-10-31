
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
        self._cache_ttl = cache_ttl
        self._hours_back = hours_back
        self._data_path = data_path
        self._cached_data: Optional[Dict[str, Any]] = None
        self._last_fetch_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._cache_file = os.path.join(
            data_path, 'data_cache.json') if data_path else None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        '''Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        '''
        if not force_refresh and self._is_cache_valid():
            return self._cached_data

        try:
            # Simulate data fetching (replace with actual implementation)
            data = self._fetch_data()
            self._set_cache(data)
            self._last_error = None
            return data
        except Exception as e:
            self._last_error = str(e)
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cached_data = None
        self._last_fetch_time = None
        if self._cache_file and os.path.exists(self._cache_file):
            os.remove(self._cache_file)

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cached_data is None or self._last_fetch_time is None:
            return False
        return (time.time() - self._last_fetch_time) < self._cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set the cache with new data.'''
        self._cached_data = data
        self._last_fetch_time = time.time()
        if self._cache_file:
            os.makedirs(os.path.dirname(self._cache_file), exist_ok=True)
            with open(self._cache_file, 'w') as f:
                json.dump({
                    'data': data,
                    'timestamp': self._last_fetch_time
                }, f)

    def _fetch_data(self) -> Dict[str, Any]:
        '''Fetch data from the source.'''
        # Replace with actual data fetching logic
        return {'data': 'sample', 'hours_back': self._hours_back}

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
        return self._last_fetch_time

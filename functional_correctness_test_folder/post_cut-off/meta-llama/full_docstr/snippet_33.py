
import os
import time
from typing import Optional, Dict, Any
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
        self.data_path = data_path or './data'
        self.cache_file = os.path.join(self.data_path, 'cache.json')
        self.last_error = None
        self.last_successful_fetch_time = None
        self._cache_timestamp = None
        self._cached_data = None

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
            return self._cached_data

        try:
            data = self._fetch_data()
            self._set_cache(data)
            self.last_error = None
            self.last_successful_fetch_time = time.time()
            return data
        except Exception as e:
            self.last_error = str(e)
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache_timestamp = None
        self._cached_data = None
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_timestamp is None:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    self._cache_timestamp = cache_data['timestamp']
                    self._cached_data = cache_data['data']
            else:
                return False

        return time.time() - self._cache_timestamp <= self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache_timestamp = time.time()
        self._cached_data = data
        with open(self.cache_file, 'w') as f:
            json.dump({'timestamp': self._cache_timestamp, 'data': data}, f)

    def _fetch_data(self) -> Dict[str, Any]:
        # Replace this with your actual data fetching logic
        # For demonstration purposes, we'll just return some dummy data
        return {'data': f'Fetched data for {self.hours_back} hours'}

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

    @last_error.setter
    def last_error(self, value: Optional[str]) -> None:
        self._last_error = value

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._last_successful_fetch_time

    @last_successful_fetch_time.setter
    def last_successful_fetch_time(self, value: Optional[float]) -> None:
        self._last_successful_fetch_time = value


import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional


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
        self.data_path = Path(data_path) if data_path else None

        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_success_time: Optional[float] = None

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
            data = self._fetch_data()
            if data is None:
                raise RuntimeError('No data returned from fetch')
            self._set_cache(data)
            self._last_error = None
            self._last_success_time = time.time()
            return data
        except Exception as exc:
            self._last_error = str(exc)
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache_data = None
        self._cache_time = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_time is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache_data = data
        self._cache_time = time.time()

    @property
    def cache_age(self) -> Optional[float]:
        '''Get age of cached data in seconds.'''
        if self._cache_time is None:
            return None
        return time.time() - self._cache_time

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._last_success_time

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _fetch_data(self) -> Optional[Dict[str, Any]]:
        '''Internal method to fetch data from the configured source.'''
        if self.data_path is None:
            # No external source configured; return dummy data
            return {
                'timestamp': time.time(),
                'hours_back': self.hours_back,
                'usage': 42,  # placeholder value
            }

        if not self.data_path.exists():
            raise FileNotFoundError(f'Data file not found: {self.data_path}')

        if self.data_path.is_dir():
            # If a directory is provided, look for a default file
            data_file = self.data_path / 'data.json'
        else:
            data_file = self.data_path

        try:
            with data_file.open('rt', encoding='utf-8') as fp:
                return json.load(fp)
        except Exception as exc:
            raise RuntimeError(
                f'Failed to read data file {data_file}: {exc}') from exc

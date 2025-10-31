from __future__ import annotations

import json
import os
import time
import threading
from typing import Any, Dict, Optional, Tuple, List


class DataManager:
    '''Manages data fetching and caching for monitoring.'''

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        '''Initialize data manager with cache and fetch settings.
        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory
        '''
        self._cache_ttl = max(0, int(cache_ttl))
        self._hours_back = int(hours_back)
        self._data_path = data_path

        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None

        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

        self._lock = threading.RLock()

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        '''Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        '''
        with self._lock:
            if not force_refresh and self._is_cache_valid():
                return self._cache_data

            try:
                data = self._fetch_data()
            except Exception as exc:
                self._last_error = str(exc) or exc.__class__.__name__
                # Return stale cache if available
                if self._cache_data is not None:
                    return self._cache_data
                return None

            if data is None:
                self._last_error = 'No data returned from fetch'
                if self._cache_data is not None:
                    return self._cache_data
                return None

            self._set_cache(data)
            self._last_error = None
            self._last_successful_fetch_time = self._cache_time
            return self._cache_data

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        with self._lock:
            self._cache_data = None
            self._cache_time = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_data is None or self._cache_time is None:
            return False
        if self._cache_ttl <= 0:
            return False
        return (time.time() - self._cache_time) <= self._cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache_data = dict(data)
        self._cache_time = time.time()

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        with self._lock:
            if self._cache_time is None:
                return float('inf')
            return max(0.0, time.time() - self._cache_time)

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        with self._lock:
            return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        with self._lock:
            return self._last_successful_fetch_time

    # Internal helpers

    def _fetch_data(self) -> Optional[Dict[str, Any]]:
        '''Fetch data from the configured source.'''
        # If no path is provided, return an empty payload indicating a successful fetch.
        if not self._data_path:
            return {
                'hours_back': self._hours_back,
                'data': [],
                'fetched_at': time.time(),
            }

        path = self._data_path

        if os.path.isdir(path):
            json_paths = [os.path.join(path, p) for p in os.listdir(
                path) if p.lower().endswith('.json')]
            if not json_paths:
                # Consider empty directory a successful fetch with empty data.
                return {
                    'hours_back': self._hours_back,
                    'data': [],
                    'fetched_at': time.time(),
                }
            # Use the most recently modified JSON file
            json_path = max(json_paths, key=lambda p: os.path.getmtime(p))
            return self._load_json_file(json_path)

        if os.path.isfile(path):
            return self._load_json_file(path)

        raise FileNotFoundError(f'Data path not found: {path}')

    def _load_json_file(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)

        # Normalize to a dict payload
        if isinstance(content, dict):
            payload = dict(content)
        elif isinstance(content, list):
            payload = {'data': content}
        else:
            raise ValueError(
                'Unsupported JSON structure: expected dict or list')

        # Ensure metadata
        payload.setdefault('hours_back', self._hours_back)
        payload.setdefault('fetched_at', time.time())
        return payload

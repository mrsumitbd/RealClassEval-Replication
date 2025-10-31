from __future__ import annotations

import json
import os
import threading
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
        self.cache_ttl = max(0, int(cache_ttl))
        self.hours_back = max(0, int(hours_back))
        self.data_path = data_path

        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

        self._lock = threading.Lock()

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

        if not force_refresh and self._cache_data is not None and self._cache_time is not None:
            stale_data: Optional[Dict[str, Any]] = self._cache_data
        else:
            stale_data = None

        try:
            data = self._fetch_data()
        except Exception as exc:
            with self._lock:
                self._last_error = f"{type(exc).__name__}: {exc}"
            return stale_data

        if not isinstance(data, dict):
            with self._lock:
                self._last_error = "Fetched data is not a dictionary"
            return stale_data

        with self._lock:
            self._set_cache(data)
        return data

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        with self._lock:
            self._cache_data = None
            self._cache_time = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_time is None:
            return False
        return (time.time() - self._cache_time) <= self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
        self._cache_data = data
        now = time.time()
        self._cache_time = now
        self._last_successful_fetch_time = now
        self._last_error = None

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        with self._lock:
            if self._cache_time is None:
                return float("inf")
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

    def _fetch_data(self) -> Dict[str, Any]:
        if self.data_path is None:
            raise FileNotFoundError("No data_path provided for fetching data")

        candidate_files = [
            os.path.join(self.data_path, "usage.json"),
            os.path.join(self.data_path, "data.json"),
        ]
        file_to_read = None
        for p in candidate_files:
            if os.path.isfile(p):
                file_to_read = p
                break

        if file_to_read is None:
            raise FileNotFoundError(f"No data file found in {self.data_path}")

        with open(file_to_read, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if isinstance(payload, dict):
            payload.setdefault("hours_back", self.hours_back)
            payload.setdefault("fetched_at", time.time())
            return payload

        raise ValueError("Data file does not contain a JSON object")


from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional


class DataManager:
    '''Manages data fetching and caching for monitoring.'''

    def __init__(
        self,
        cache_ttl: int = 30,
        hours_back: int = 192,
        data_path: Optional[str] = None,
    ) -> None:
        '''Initialize data manager with cache and fetch settings.
        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory or file
        '''
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = Path(data_path) if data_path else None

        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_timestamp: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        '''Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        '''
        if force_refresh or not self._is_cache_valid():
            try:
                data = self._fetch_data()
                self._set_cache(data)
                self._last_error = None
                self._last_successful_fetch_time = time.time()
                return data
            except Exception as exc:
                self._last_error = str(exc)
                return None
        return self._cache_data

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache_data = None
        self._cache_timestamp = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_data is None or self._cache_timestamp is None:
            return False
        age = time.time() - self._cache_timestamp
        return age < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        '''Set cache with current timestamp.'''
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

    # --------------------------------------------------------------------
    # Internal helpers
    # --------------------------------------------------------------------
    def _fetch_data(self) -> Dict[str, Any]:
        '''Internal method to fetch data from the configured source.'''
        if self.data_path is None:
            # No external source configured – return dummy data
            return {
                "timestamp": time.time(),
                "value": 42,
                "source": "dummy",
            }

        if self.data_path.is_file():
            return self._read_json_file(self.data_path)

        if self.data_path.is_dir():
            # Find the most recent JSON file within the directory
            json_files = sorted(
                (p for p in self.data_path.glob("*.json") if p.is_file()),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if not json_files:
                raise FileNotFoundError(
                    f"No JSON files found in directory {self.data_path}")
            return self._read_json_file(json_files[0])

        raise FileNotFoundError(f"Data path {self.data_path} does not exist")

    @staticmethod
    def _read_json_file(path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)

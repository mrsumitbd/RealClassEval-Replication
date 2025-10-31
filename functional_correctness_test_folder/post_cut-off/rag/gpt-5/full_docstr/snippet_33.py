from __future__ import annotations

import json
import os
import threading
import time
from typing import Any, Dict, Optional


class DataManager:
    """Manages data fetching and caching for monitoring."""

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        """Initialize data manager with cache and fetch settings.
        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory
        """
        self.cache_ttl = max(0, int(cache_ttl))
        self.hours_back = max(0, int(hours_back))
        self.data_path = data_path

        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

        self._lock = threading.Lock()

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        """
        with self._lock:
            if not force_refresh and self._is_cache_valid():
                return self._cache_data

            try:
                data = self._fetch_data()
                self._set_cache(data)
                self._last_error = None
                self._last_successful_fetch_time = self._cache_time
                return data
            except Exception as e:
                self._last_error = str(e)
                # Fallback to any available cached data even if stale
                return self._cache_data

    def invalidate_cache(self) -> None:
        """Invalidate the cache."""
        with self._lock:
            self._cache_data = None
            self._cache_time = None

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if self._cache_time is None or self._cache_data is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        """Set cache with current timestamp."""
        self._cache_data = data
        self._cache_time = time.time()

    @property
    def cache_age(self) -> float:
        """Get age of cached data in seconds."""
        if self._cache_time is None:
            return 0.0
        return max(0.0, time.time() - self._cache_time)

    @property
    def last_error(self) -> Optional[str]:
        """Get last error message."""
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        """Get timestamp of last successful fetch."""
        return self._last_successful_fetch_time

    # Internal helpers

    def _fetch_data(self) -> Dict[str, Any]:
        """Fetch data from source.

        Default implementation loads JSON from data_path. If data_path is a directory,
        it will try 'usage.json' then 'data.json' inside that directory.

        Raises:
            RuntimeError: If data_path is not set or file cannot be found/read.
            ValueError: If JSON content is invalid.
        """
        if not self.data_path:
            raise RuntimeError("No data_path configured for DataManager")

        path = self.data_path
        if os.path.isdir(path):
            candidates = [
                os.path.join(path, "usage.json"),
                os.path.join(path, "data.json"),
            ]
            for p in candidates:
                if os.path.isfile(p):
                    path = p
                    break
            else:
                raise RuntimeError(
                    f"No data file found in directory: {self.data_path}")
        else:
            if not os.path.isfile(path):
                raise RuntimeError(f"Data file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("Data must be a JSON object at top level")

        # Optionally, we could trim data based on hours_back here if format supports it.
        return data

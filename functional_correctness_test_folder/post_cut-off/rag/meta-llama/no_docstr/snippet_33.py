
from typing import Any, Dict, Optional
import time
import os
import json


class DataManager:
    """Manages data fetching and caching for monitoring."""

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        """Initialize data manager with cache and fetch settings.

        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory
        """
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = data_path or './data'
        self._cache_file = os.path.join(self.data_path, 'cache.json')
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None
        self._cache_timestamp: Optional[float] = None
        self._cached_data: Optional[Dict[str, Any]] = None

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Get monitoring data with caching and error handling.

        Args:
            force_refresh: Force refresh ignoring cache

        Returns:
            Usage data dictionary or None if fetch fails
        """
        if not force_refresh and self._is_cache_valid():
            return self._cached_data

        try:
            data = self._fetch_data()
            self._set_cache(data)
            self._last_error = None
            self._last_successful_fetch_time = time.time()
            return data
        except Exception as e:
            self._last_error = str(e)
            return None

    def invalidate_cache(self) -> None:
        """Invalidate the cache."""
        self._cache_timestamp = None
        self._cached_data = None
        if os.path.exists(self._cache_file):
            os.remove(self._cache_file)

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if self._cache_timestamp is None or self._cached_data is None:
            if os.path.exists(self._cache_file):
                with open(self._cache_file, 'r') as f:
                    cache_data = json.load(f)
                    self._cache_timestamp = cache_data['timestamp']
                    self._cached_data = cache_data['data']
            else:
                return False

        return time.time() - self._cache_timestamp <= self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        """Set cache with current timestamp."""
        self._cache_timestamp = time.time()
        self._cached_data = data
        with open(self._cache_file, 'w') as f:
            json.dump({'timestamp': self._cache_timestamp, 'data': data}, f)

    @property
    def cache_age(self) -> float:
        """Get age of cached data in seconds."""
        if self._cache_timestamp is None:
            return float('inf')
        return time.time() - self._cache_timestamp

    @property
    def last_error(self) -> Optional[str]:
        """Get last error message."""
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        """Get timestamp of last successful fetch."""
        return self._last_successful_fetch_time

    def _fetch_data(self) -> Dict[str, Any]:
        # This method should be implemented to fetch the actual data
        # For demonstration purposes, it returns an empty dictionary
        return {}

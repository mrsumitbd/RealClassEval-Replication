
import time
from typing import Dict, Any, Optional
import json
import os


class DataManager:

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = data_path if data_path else "data_cache.json"
        self._cache_data = None
        self._last_fetch_time = None
        self._last_error = None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        if force_refresh or not self._is_cache_valid():
            try:
                # Simulate fetching data from an external source
                data = self._fetch_data()
                self._set_cache(data)
                self._last_fetch_time = time.time()
                self._last_error = None
            except Exception as e:
                self._last_error = str(e)
                return None
        return self._cache_data

    def invalidate_cache(self) -> None:
        self._cache_data = None
        self._last_fetch_time = None

    def _is_cache_valid(self) -> bool:
        if self._cache_data is None or self._last_fetch_time is None:
            return False
        return (time.time() - self._last_fetch_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        self._cache_data = data
        with open(self.data_path, 'w') as f:
            json.dump(data, f)

    def _fetch_data(self) -> Dict[str, Any]:
        # Simulate fetching data from an external source
        # In a real implementation, this would be replaced with actual data fetching logic
        data = {
            "timestamp": time.time(),
            "data": "sample data"
        }
        return data

    @property
    def cache_age(self) -> float:
        if self._last_fetch_time is None:
            return float('inf')
        return time.time() - self._last_fetch_time

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        return self._last_fetch_time

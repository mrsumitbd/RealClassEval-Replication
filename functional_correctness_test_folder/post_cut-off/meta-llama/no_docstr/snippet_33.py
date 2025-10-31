
import os
import json
import time
from typing import Optional, Dict, Any


class DataManager:

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = data_path if data_path else os.path.join(
            os.getcwd(), 'data_cache.json')
        self._cache = None
        self._cache_timestamp = None
        self._last_error = None
        self._last_successful_fetch_time = None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        if force_refresh or not self._is_cache_valid():
            try:
                # Simulating data fetching, replace with actual data fetching logic
                data = self._fetch_data()
                self._set_cache(data)
                self._last_successful_fetch_time = time.time()
                self._last_error = None
            except Exception as e:
                self._last_error = str(e)
                return None
        return self._cache

    def invalidate_cache(self) -> None:
        self._cache = None
        self._cache_timestamp = None
        if os.path.exists(self.data_path):
            os.remove(self.data_path)

    def _is_cache_valid(self) -> bool:
        if self._cache is None or self._cache_timestamp is None:
            if os.path.exists(self.data_path):
                self._cache_timestamp = os.path.getmtime(self.data_path)
                with open(self.data_path, 'r') as f:
                    self._cache = json.load(f)
            else:
                return False
        return time.time() - self._cache_timestamp < self.cache_ttl * 60

    def _set_cache(self, data: Dict[str, Any]) -> None:
        self._cache = data
        self._cache_timestamp = time.time()
        with open(self.data_path, 'w') as f:
            json.dump(data, f)

    @property
    def cache_age(self) -> float:
        if self._cache_timestamp is None:
            return float('inf')
        return time.time() - self._cache_timestamp

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        return self._last_successful_fetch_time

    def _fetch_data(self) -> Dict[str, Any]:
        # Replace this with your actual data fetching logic
        # For demonstration purposes, it returns a dummy data
        return {'data': 'dummy_data'}

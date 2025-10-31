
import os
import json
import time
from typing import Optional, Dict, Any


class DataManager:

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        self._cache_ttl = cache_ttl
        self._hours_back = hours_back
        self._data_path = data_path or os.path.join(
            os.getcwd(), "data_cache.json")
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None
        self._cache_data: Optional[Dict[str, Any]] = None
        self._load_cache()

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        if not force_refresh and self._is_cache_valid():
            return self._cache_data

        try:
            # Simulate fetching data (replace with actual data fetching logic)
            data = {"sample_key": "sample_value", "timestamp": time.time()}
            self._set_cache(data)
            self._last_error = None
            self._last_successful_fetch_time = time.time()
            return data
        except Exception as e:
            self._last_error = str(e)
            return None

    def invalidate_cache(self) -> None:
        self._cache_data = None
        self._last_successful_fetch_time = None
        if os.path.exists(self._data_path):
            os.remove(self._data_path)

    def _is_cache_valid(self) -> bool:
        if self._cache_data is None:
            return False
        if self._last_successful_fetch_time is None:
            return False
        return (time.time() - self._last_successful_fetch_time) < (self._cache_ttl * 60)

    def _set_cache(self, data: Dict[str, Any]) -> None:
        self._cache_data = data
        self._last_successful_fetch_time = time.time()
        with open(self._data_path, 'w') as f:
            json.dump(data, f)

    def _load_cache(self) -> None:
        if os.path.exists(self._data_path):
            try:
                with open(self._data_path, 'r') as f:
                    self._cache_data = json.load(f)
                    if isinstance(self._cache_data, dict) and "timestamp" in self._cache_data:
                        self._last_successful_fetch_time = self._cache_data["timestamp"]
            except Exception as e:
                self._last_error = str(e)
                self._cache_data = None

    @property
    def cache_age(self) -> float:
        if self._last_successful_fetch_time is None:
            return float('inf')
        return time.time() - self._last_successful_fetch_time

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        return self._last_successful_fetch_time

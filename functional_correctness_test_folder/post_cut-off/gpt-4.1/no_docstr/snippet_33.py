
import os
import time
import json
from typing import Optional, Dict, Any


class DataManager:

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = data_path or "data_manager_cache.json"
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None
        self._load_cache_from_disk()

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        if not force_refresh and self._is_cache_valid():
            return self._cache
        try:
            # Simulate data fetching
            data = {
                "timestamp": time.time(),
                "hours_back": self.hours_back,
                "data": [i for i in range(self.hours_back)]
            }
            self._set_cache(data)
            self._last_error = None
            self._last_successful_fetch_time = time.time()
            return data
        except Exception as e:
            self._last_error = str(e)
            return None

    def invalidate_cache(self) -> None:
        self._cache = None
        self._cache_time = None
        if os.path.exists(self.data_path):
            try:
                os.remove(self.data_path)
            except Exception:
                pass

    def _is_cache_valid(self) -> bool:
        if self._cache is None or self._cache_time is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        self._cache = data
        self._cache_time = time.time()
        try:
            with open(self.data_path, "w") as f:
                json.dump({
                    "cache": self._cache,
                    "cache_time": self._cache_time
                }, f)
        except Exception as e:
            self._last_error = str(e)

    def _load_cache_from_disk(self) -> None:
        if not os.path.exists(self.data_path):
            return
        try:
            with open(self.data_path, "r") as f:
                obj = json.load(f)
                self._cache = obj.get("cache")
                self._cache_time = obj.get("cache_time")
        except Exception as e:
            self._cache = None
            self._cache_time = None
            self._last_error = str(e)

    @property
    def cache_age(self) -> float:
        if self._cache_time is None:
            return float('inf')
        return time.time() - self._cache_time

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        return self._last_successful_fetch_time


import json
import os
import time
from typing import Any, Dict, Optional


class DataManager:
    def __init__(
        self,
        cache_ttl: int = 30,
        hours_back: int = 192,
        data_path: Optional[str] = None,
    ) -> None:
        """
        Initialize the DataManager.

        :param cache_ttl: Time-to-live for the cache in seconds.
        :param hours_back: (Unused in this implementation but kept for API compatibility)
        :param data_path: Path to a JSON file containing the data. If None, dummy data is generated.
        """
        self.cache_ttl = cache_ttl
        self.hours_back = hours_back
        self.data_path = data_path

        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Retrieve data, using the cache if valid unless force_refresh is True.

        :param force_refresh: If True, bypass the cache and fetch fresh data.
        :return: The data dictionary or None if fetching failed.
        """
        if not force_refresh and self._is_cache_valid():
            return self._cache_data

        try:
            if self.data_path and os.path.isfile(self.data_path):
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                # Dummy data generation
                data = {"timestamp": time.time(), "value": 42}

            self._set_cache(data)
            self._last_error = None
            self._last_successful_fetch_time = time.time()
            return data
        except Exception as exc:
            self._last_error = str(exc)
            return None

    def invalidate_cache(self) -> None:
        """
        Invalidate the current cache.
        """
        self._cache_data = None
        self._cache_time = None

    def _is_cache_valid(self) -> bool:
        """
        Check if the cache is still valid based on TTL.

        :return: True if cache exists and is within TTL, False otherwise.
        """
        if self._cache_data is None or self._cache_time is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        """
        Store data in the cache with the current timestamp.

        :param data: The data dictionary to cache.
        """
        self._cache_data = data
        self._cache_time = time.time()

    @property
    def cache_age(self) -> float:
        """
        Return the age of the cache in seconds.

        :return: Age in seconds, or 0.0 if no cache.
        """
        if self._cache_time is None:
            return 0.0
        return time.time() - self._cache_time

    @property
    def last_error(self) -> Optional[str]:
        """
        Return the last error message encountered during data fetching.

        :return: Error string or None.
        """
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        """
        Return the timestamp of the last successful data fetch.

        :return: Timestamp in seconds since epoch or None.
        """
        return self._last_successful_fetch_time

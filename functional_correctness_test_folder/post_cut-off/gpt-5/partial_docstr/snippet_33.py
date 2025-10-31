from __future__ import annotations

import json
import os
import time
from glob import glob
from typing import Any, Dict, Optional, List


class DataManager:
    '''Manages data fetching and caching for monitoring.'''

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        '''Initialize data manager with cache and fetch settings.
        Args:
            cache_ttl: Cache time-to-live in seconds
            hours_back: Hours of historical data to fetch
            data_path: Path to data directory
        '''
        self.cache_ttl: int = max(0, int(cache_ttl))
        self.hours_back: int = max(0, int(hours_back))
        self.data_path: Optional[str] = data_path

        self._cache_data: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_success_ts: Optional[float] = None

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        '''Get monitoring data with caching and error handling.
        Args:
            force_refresh: Force refresh ignoring cache
        Returns:
            Usage data dictionary or None if fetch fails
        '''
        if not force_refresh and self._is_cache_valid():
            return self._cache_data

        try:
            data = self._fetch_data()
            if not isinstance(data, dict):
                raise ValueError("Fetched data is not a dictionary")
            self._set_cache(data)
            return data
        except Exception as exc:
            self._last_error = f"{type(exc).__name__}: {exc}"
            # Fallback to stale cache if available
            if self._cache_data is not None:
                return self._cache_data
            return None

    def invalidate_cache(self) -> None:
        '''Invalidate the cache.'''
        self._cache_time = None
        self._cache_data = None

    def _is_cache_valid(self) -> bool:
        '''Check if cache is still valid.'''
        if self._cache_time is None or self._cache_data is None:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        self._cache_data = data
        self._cache_time = time.time()
        self._last_error = None
        self._last_success_ts = self._cache_time

    @property
    def cache_age(self) -> float:
        '''Get age of cached data in seconds.'''
        if self._cache_time is None:
            return float("inf")
        return max(0.0, time.time() - self._cache_time)

    @property
    def last_error(self) -> Optional[str]:
        '''Get last error message.'''
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        '''Get timestamp of last successful fetch.'''
        return self._last_success_ts

    def _fetch_data(self) -> Dict[str, Any]:
        now = time.time()
        horizon = now - (self.hours_back * 3600)

        # If a path is provided, attempt to load data from JSON files
        if self.data_path:
            path = os.path.abspath(self.data_path)

            if not os.path.exists(path):
                raise FileNotFoundError(f"Data path not found: {path}")

            # Try common filenames first
            for fname in ("usage.json", "data.json"):
                candidate = os.path.join(path, fname)
                if os.path.isfile(candidate):
                    with open(candidate, "r", encoding="utf-8") as f:
                        payload = json.load(f)
                    return {
                        "source": os.path.basename(candidate),
                        "loaded_at": now,
                        "data": payload,
                    }

            # Fallback: aggregate recent JSON files
            json_files: List[str] = sorted(glob(os.path.join(path, "*.json")))
            recent_files = [
                p for p in json_files if os.path.getmtime(p) >= horizon]

            aggregated: List[Dict[str, Any]] = []
            for p in recent_files:
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        content = json.load(f)
                    aggregated.append(
                        {
                            "file": os.path.basename(p),
                            "mtime": os.path.getmtime(p),
                            "data": content,
                        }
                    )
                except Exception as e:
                    # Continue on per-file errors; overall fetch can still succeed
                    if self._last_error is None:
                        self._last_error = f"{type(e).__name__} reading {p}: {e}"

            return {
                "source": os.path.abspath(path),
                "loaded_at": now,
                "window_start": horizon,
                "files_count": len(recent_files),
                "entries": aggregated,
            }

        # No data_path: return a minimal heartbeat structure
        return {
            "source": "generated",
            "loaded_at": now,
            "window_start": horizon,
            "message": "No data_path provided; returning heartbeat payload.",
        }

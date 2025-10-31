from typing import Optional, Dict, Any
import time
import json
import os
import tempfile
import errno


class DataManager:

    def __init__(self, cache_ttl: int = 30, hours_back: int = 192, data_path: Optional[str] = None) -> None:
        self._cache_ttl = max(0, int(cache_ttl))
        self._hours_back = int(hours_back)
        self._data_path = data_path
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None
        self._last_error: Optional[str] = None
        self._last_successful_fetch_time: Optional[float] = None

        if self._data_path:
            self._load_cache_from_disk()

    def get_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        if not force_refresh and self._is_cache_valid():
            return self._cache

        try:
            data = self._fetch_data()
            if data is not None:
                self._set_cache(data)
                self._last_successful_fetch_time = time.time()
                self._last_error = None
                return data
            else:
                self._last_error = "Fetch returned no data."
        except NotImplementedError:
            self._last_error = "Fetch method not implemented."
        except Exception as e:
            self._last_error = f"Fetch failed: {e}"

        if self._is_cache_valid():
            return self._cache
        return None

    def invalidate_cache(self) -> None:
        self._cache = None
        self._cache_time = None
        if self._data_path:
            try:
                os.remove(self._data_path)
            except FileNotFoundError:
                pass
            except Exception:
                pass

    def _is_cache_valid(self) -> bool:
        if self._cache is None or self._cache_time is None:
            return False
        return (time.time() - self._cache_time) <= self._cache_ttl

    def _set_cache(self, data: Dict[str, Any]) -> None:
        self._cache = data
        self._cache_time = time.time()
        if self._data_path:
            self._save_cache_to_disk()

    @property
    def cache_age(self) -> float:
        if self._cache_time is None:
            return float("inf")
        return max(0.0, time.time() - self._cache_time)

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    @property
    def last_successful_fetch_time(self) -> Optional[float]:
        return self._last_successful_fetch_time

    def _fetch_data(self) -> Optional[Dict[str, Any]]:
        raise NotImplementedError(
            "Override _fetch_data to implement data retrieval")

    def _load_cache_from_disk(self) -> None:
        try:
            with open(self._data_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            ts = payload.get("timestamp")
            data = payload.get("data")
            if isinstance(ts, (int, float)) and isinstance(data, dict):
                self._cache_time = float(ts)
                self._cache = data
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            self._last_error = "Cache file is corrupted."
        except Exception as e:
            self._last_error = f"Failed to load cache: {e}"

    def _save_cache_to_disk(self) -> None:
        if self._cache is None or self._cache_time is None:
            return
        payload = {"timestamp": self._cache_time, "data": self._cache}
        directory = os.path.dirname(self._data_path) if self._data_path else ""
        if directory:
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    self._last_error = f"Failed to create cache directory: {e}"
                    return
        try:
            dir_for_temp = directory if directory else "."
            with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_for_temp, encoding="utf-8") as tf:
                json.dump(payload, tf)
                temp_name = tf.name
            os.replace(temp_name, self._data_path)
        except Exception as e:
            self._last_error = f"Failed to write cache: {e}"
            try:
                if 'temp_name' in locals():
                    os.unlink(temp_name)
            except Exception:
                pass

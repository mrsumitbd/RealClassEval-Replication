import os
from typing import Any, Iterable, Optional, Tuple, Union

try:
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.windows import Window
    _HAS_RASTERIO = True
except Exception:  # pragma: no cover
    _HAS_RASTERIO = False
    rasterio = None
    Resampling = None
    Window = None


class RIODataset:
    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        self.ds = None
        self.path = None
        self._closed = True
        self._writeable = False

        if not _HAS_RASTERIO:
            raise RuntimeError("rasterio is required to use RIODataset")

        if hasattr(rfile, "close") and hasattr(rfile, "read"):
            self.ds = rfile
            self._closed = False
            try:
                # Writer has write methods, reader doesn't
                self._writeable = hasattr(self.ds, "write")
            except Exception:
                self._writeable = False
        else:
            self.path = str(rfile)
            # Try r+ first for overviews or potential writes
            self.ds = self._open_prefer_rw(self.path)
            self._closed = False

        if overviews is not None:
            try:
                self._ensure_writeable()
                factors = self._normalize_overview_factors(
                    overviews, overviews_minsize)
                if factors:
                    method = self._normalize_resampling(overviews_resampling)
                    self.ds.build_overviews(factors, method)
                    try:
                        self.ds.update_tags(ns="rio_overviews",
                                            factors=",".join(
                                                map(str, factors)),
                                            resampling=method.name)
                    except Exception:
                        pass
                    try:
                        self.ds._close()  # flush internal caches for some drivers
                        self.ds = self._reopen_same_mode(self.ds)
                    except Exception:
                        pass
            except Exception:
                # Best-effort; ignore if building overviews fails
                pass

    def __setitem__(self, key, item):
        self._ensure_writeable()

        # Supported patterns:
        # - int band index
        # - iterable of band indices
        # - (indexes, window) where indexes is int or iterable; window is rasterio Window or tuple
        indexes: Optional[Union[int, Iterable[int]]] = None
        window: Optional[Any] = None

        if isinstance(key, tuple) and len(key) == 2:
            indexes, window = key
        else:
            indexes = key

        if window is not None and not isinstance(window, Window):
            # Accept ((row_off, col_off), (height, width)) or (row_off, col_off, height, width)
            if isinstance(window, tuple):
                if len(window) == 2 and all(isinstance(x, tuple) for x in window):
                    window = Window.from_slices(
                        slice(window[0][0], window[0][0] + window[1][0]),
                        slice(window[0][1], window[0][1] + window[1][1]),
                    )
                elif len(window) == 4:
                    window = Window(window[0], window[1], window[2], window[3])

        self.ds.write(item, indexes=indexes, window=window)

    def close(self):
        if getattr(self, "ds", None) is not None and not self._closed:
            try:
                self.ds.close()
            finally:
                self._closed = True

    # Internal helpers

    def _open_prefer_rw(self, path: str):
        ds = None
        # Try r+
        try:
            ds = rasterio.open(path, "r+")
            self._writeable = True
            return ds
        except Exception:
            pass
        # Fall back to r
        ds = rasterio.open(path, "r")
        self._writeable = False
        return ds

    def _reopen_same_mode(self, ds):
        path = getattr(ds, "name", None) or self.path
        mode = getattr(ds, "mode", "r")
        try:
            reopened = rasterio.open(path, mode)
            self._writeable = hasattr(reopened, "write")
            return reopened
        except Exception:
            return ds

    def _ensure_writeable(self):
        if self._writeable:
            return
        # Try to reopen in r+ if possible
        name = getattr(self.ds, "name", None) or self.path
        if name is not None:
            try:
                reopened = rasterio.open(name, "r+")
                try:
                    self.ds.close()
                except Exception:
                    pass
                self.ds = reopened
                self._writeable = True
                self._closed = False
                return
            except Exception:
                pass
        raise IOError(
            "Dataset is not open in write mode; cannot perform write operation.")

    def _normalize_overview_factors(self, overviews, minsize: int):
        if overviews is True or overviews == "auto":
            w = getattr(self.ds, "width", None)
            h = getattr(self.ds, "height", None)
            if not w or not h:
                return []
            factors = []
            f = 2
            while max(w // f, h // f) >= int(minsize):
                factors.append(f)
                f *= 2
            return factors
        if isinstance(overviews, (list, tuple)):
            return [int(x) for x in overviews if int(x) > 1]
        if isinstance(overviews, int):
            return [int(overviews)] if overviews > 1 else []
        return []

    def _normalize_resampling(self, method):
        if method is None:
            method = "nearest"
        if isinstance(method, Resampling):
            return method
        name = str(method).lower()
        # Map common aliases
        alias = {
            "nearest": "nearest",
            "mode": "mode",
            "avg": "average",
            "average": "average",
            "bilinear": "bilinear",
            "cubic": "cubic",
            "cubic_spline": "cubic_spline",
            "lanczos": "lanczos",
            "min": "min",
            "max": "max",
            "med": "med",
            "median": "med",
            "q1": "q1",
            "q3": "q3",
            "sum": "sum",
        }
        key = alias.get(name, name)
        try:
            return getattr(Resampling, key)
        except Exception:
            return Resampling.nearest

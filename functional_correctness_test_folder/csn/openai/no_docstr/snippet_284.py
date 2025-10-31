
import rasterio
from rasterio.enums import Resampling
from rasterio.errors import RasterioIOError


class RIODataset:
    """
    A lightweight wrapper around rasterio that supports optional overview creation
    and simple band‑wise write operations via the ``__setitem__`` interface.
    """

    def __init__(
        self,
        rfile,
        overviews=None,
        overviews_resampling=None,
        overviews_minsize=256,
    ):
        """
        Parameters
        ----------
        rfile : str or pathlib.Path
            Path to the raster file to open.
        overviews : list[int] | None
            List of overview levels to build. If ``None`` no overviews are built.
        overviews_resampling : rasterio.enums.Resampling | None
            Resampling method used when building overviews. Defaults to
            ``Resampling.nearest``.
        overviews_minsize : int
            Minimum size of the smallest overview. This is passed to
            ``build_overviews`` via the ``min_size`` keyword.
        """
        self.rfile = rfile
        self.overviews = overviews
        self.overviews_resampling = (
            overviews_resampling or Resampling.nearest
        )
        self.overviews_minsize = overviews_minsize

        try:
            self.ds = rasterio.open(rfile, "r+")
        except RasterioIOError as exc:
            raise FileNotFoundError(
                f"Could not open raster file {rfile}") from exc

        # Build overviews if requested and they do not already exist
        if self.overviews:
            # Check if any overviews exist for the first band
            existing = self.ds.overviews(1)
            if not existing:
                self.ds.build_overviews(
                    self.overviews,
                    self.overviews_resampling,
                    min_size=self.overviews_minsize,
                )
                # Store the resampling method in the tags for future reference
                self.ds.update_tags(1, OVERVIEW_RESAMPLING=str(
                    self.overviews_resampling))

        # Cache some useful attributes
        self.shape = self.ds.shape
        self.count = self.ds.count
        self.dtypes = self.ds.dtypes

    def __setitem__(self, key, item):
        """
        Write data to one or more bands.

        Parameters
        ----------
        key : int | slice
            Band index (1‑based) or slice of band indices.
        item : array-like
            Data to write. For a single band the shape must be
            (height, width). For a slice the shape must be
            (num_bands, height, width).
        """
        if isinstance(key, int):
            band = key
            if band < 1 or band > self.count:
                raise IndexError(
                    f"Band index {band} out of range (1–{self.count})")
            self.ds.write(item, band)
        elif isinstance(key, slice):
            start = key.start or 1
            stop = key.stop or self.count + 1
            step = key.step or 1
            bands = list(range(start, stop, step))
            if any(b < 1 or b > self.count for b in bands):
                raise IndexError(
                    f"Band indices {bands} out of range (1–{self.count})")
            self.ds.write(item, bands)
        else:
            raise TypeError("Key must be an int (band) or slice of bands")

    def close(self):
        """Close the underlying rasterio dataset."""
        if hasattr(self, "ds") and self.ds:
            self.ds.close()
            self.ds = None

    # Optional context‑manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

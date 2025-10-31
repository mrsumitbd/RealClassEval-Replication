
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window
import numpy as np


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        # Open the dataset in read/write mode
        self.ds = rasterio.open(rfile, mode='r+')

        # Store overview settings
        self.overviews_minsize = overviews_minsize
        self.overviews_resampling = (
            overviews_resampling if overviews_resampling is not None
            else Resampling.bilinear
        )

        # Build overviews if requested
        if overviews is not None:
            # Ensure overviews is a list of integers
            if isinstance(overviews, int):
                overviews = [overviews]
            self.ds.build_overviews(
                overviews, resampling=self.overviews_resampling)

    def __setitem__(self, key, item):
        """
        Write data to the dataset.

        Parameters
        ----------
        key : tuple of slice objects or a Window
            The window (row, col) slice to write to.
        item : array-like
            Data to write. Can be 2‑D (height, width) for a single band
            or 3‑D (bands, height, width) for multiple bands.
        """
        # Convert key to a Window if it is a tuple of slices
        if isinstance(key, tuple) and all(isinstance(s, slice) for s in key):
            # Expect key to be (row_slice, col_slice) or (row_slice, col_slice, band_slice)
            if len(key) == 2:
                row_slice, col_slice = key
                band_slice = slice(None)
            elif len(key) == 3:
                row_slice, col_slice, band_slice = key
            else:
                raise ValueError(
                    "Key must be a tuple of 2 or 3 slice objects.")
            window = Window.from_slices((row_slice, col_slice))
        elif isinstance(key, Window):
            window = key
            band_slice = slice(None)
        else:
            raise TypeError(
                "Key must be a tuple of slices or a rasterio.windows.Window.")

        # Prepare data array
        data = np.asarray(item)

        # Determine which bands to write
        if data.ndim == 2:
            # Single band
            bands = [1]
            data_to_write = data
        elif data.ndim == 3:
            # Multiple bands
            bands = list(range(1, data.shape[0] + 1))
            data_to_write = data
        else:
            raise ValueError("Data must be 2‑D or 3‑D array.")

        # Write data
        self.ds.write(data_to_write, indexes=bands, window=window)

    def close(self):
        '''Close the file.'''
        self.ds.close()

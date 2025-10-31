
import rasterio
from rasterio.enums import Resampling
import numpy as np


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        # Open the dataset in read/write mode
        self.dataset = rasterio.open(rfile, mode='r+')

        # Build overviews if requested
        if overviews is not None:
            # Default resampling method
            if overviews_resampling is None:
                overviews_resampling = Resampling.nearest

            # Filter out overviews that would produce images smaller than the minimum size
            filtered_overviews = []
            for ov in overviews:
                # Compute the size of the overview
                w = max(self.dataset.width // ov, 1)
                h = max(self.dataset.height // ov, 1)
                if max(w, h) >= overviews_minsize:
                    filtered_overviews.append(ov)

            if filtered_overviews:
                self.dataset.build_overviews(
                    filtered_overviews, resampling=overviews_resampling)
                # Store the resampling method in the dataset tags for reference
                self.dataset.update_tags(
                    ns='rio_overview', resampling=overviews_resampling.name)

    def __setitem__(self, key, item):
        '''Put the data chunk in the image.'''
        # Ensure the item is a NumPy array
        if not isinstance(item, np.ndarray):
            item = np.asarray(item)

        # Write the array to the dataset at the specified window
        # If the dataset has multiple bands, write to all bands
        if self.dataset.count == 1:
            self.dataset.write(item, window=key)
        else:
            # Broadcast the item to match the number of bands if necessary
            if item.ndim == 2:
                # Expand dims to match bands
                item = np.expand_dims(item, axis=0)
            if item.shape[0] != self.dataset.count:
                raise ValueError(
                    f"Item has {item.shape[0]} bands, but dataset has {self.dataset.count} bands.")
            self.dataset.write(item, window=key)

    def close(self):
        '''Close the file.'''
        if self.dataset is not None:
            self.dataset.close()
            self.dataset = None

    def __del__(self):
        # Ensure the dataset is closed when the object is garbage collected
        try:
            self.close()
        except Exception:
            pass

from rasterio.profiles import Profile
from mapchete.io.raster.write import _write_tags
from rasterio.io import DatasetReader, DatasetWriter, MemoryFile
from mapchete.validate import validate_write_window_params
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union
from mapchete.io.raster.array import extract_from_array, prepare_masked_array
from mapchete.tile import BufferedTile
import numpy.ma as ma

class RasterWindowMemoryFile:
    """Context manager around rasterio.io.MemoryFile."""

    def __init__(self, in_tile: BufferedTile, in_data: ma.MaskedArray, out_profile: Profile, out_tile: Optional[BufferedTile]=None, tags: Optional[Dict[str, Any]]=None):
        """Prepare data & profile."""
        out_tile = out_tile or in_tile
        validate_write_window_params(in_tile, out_tile, in_data, out_profile)
        self.data = extract_from_array(array=in_data, in_affine=in_tile.affine, out_tile=out_tile)
        if 'affine' in out_profile:
            out_profile['transform'] = out_profile.pop('affine')
        self.profile = out_profile
        self.tags = tags

    def __enter__(self):
        """Open MemoryFile, write data and return."""
        self.rio_memfile = MemoryFile()
        with self.rio_memfile.open(**self.profile) as dst:
            dst.write(self.data.astype(self.profile['dtype'], copy=False))
            _write_tags(dst, self.tags)
        return self.rio_memfile

    def __exit__(self, *args):
        """Make sure MemoryFile is closed."""
        self.rio_memfile.close()
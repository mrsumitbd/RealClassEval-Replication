from mapchete.path import MPath
from shapely.geometry import shape
from itertools import chain
from mapchete.tile import BufferedTile, BufferedTilePyramid
from pydantic import NonNegativeInt
from typing import Any, List, Optional, Tuple
from mapchete.types import CRSLike
import warnings
from mapchete.io.raster import create_mosaic, extract_from_array, prepare_array, read_raster_window

class OutputDataBase:
    write_in_parent_process = False
    pixelbuffer: NonNegativeInt
    pyramid: BufferedTilePyramid
    crs: CRSLike

    def __init__(self, output_params: dict, readonly: bool=False, **kwargs):
        """Initialize."""
        self.pixelbuffer = output_params['pixelbuffer']
        if 'type' in output_params:
            warnings.warn(DeprecationWarning("'type' is deprecated and should be 'grid'"))
            if 'grid' not in output_params:
                output_params['grid'] = output_params.pop('type')
        self.pyramid = BufferedTilePyramid(grid=output_params['grid'], metatiling=output_params['metatiling'], pixelbuffer=output_params['pixelbuffer'], tile_size=output_params.get('tile_size', 256))
        self.crs = self.pyramid.crs
        self.storage_options = output_params.get('storage_options')

    def get_path(self, tile: BufferedTile) -> MPath:
        """
        Determine target file path.

        Parameters
        ----------
        tile : ``BufferedTile``
            must be member of output ``TilePyramid``

        Returns
        -------
        path : string
        """
        return self.path / self.tile_path_schema.format(zoom=str(tile.zoom), row=str(tile.row), col=str(tile.col), extension=self.file_extension.lstrip('.'))

    def extract_subset(self, input_data_tiles: List[Tuple[BufferedTile, Any]], out_tile: BufferedTile) -> Any:
        """
        Extract subset from multiple tiles.
        input_data_tiles : list of (``Tile``, process data) tuples
        out_tile : ``Tile``
        Returns
        -------
        NumPy array or list of features.
        """
        if self.METADATA['data_type'] == 'raster':
            mosaic = create_mosaic(input_data_tiles)
            return extract_from_array(array=prepare_array(mosaic.data, nodata=self.output_params['nodata'], dtype=self.output_params['dtype']), in_affine=mosaic.affine, out_tile=out_tile)
        elif self.METADATA['data_type'] == 'vector':
            return [feature for feature in list(chain.from_iterable([features for _, features in input_data_tiles])) if shape(feature['geometry']).intersects(out_tile.bbox)]

    def prepare(self, **kwargs):
        pass
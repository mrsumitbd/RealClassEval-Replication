
import pathlib
from typing import Dict, List, Union

import attr
import numpy as np

from rio_tiler.colormap import DEFAULTS_CMAPS

ColorMapType = Dict[int,
                    Union[Tuple[int, int, int], Tuple[int, int, int, int]]]


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(default=DEFAULTS_CMAPS)

    def get(self, name: str) -> ColorMapType:
        '''Fetch a colormap.
        Args:
            name (str): colormap name.
        Returns
            dict: colormap dictionary.
        '''
        return self.data[name]

    def list(self) -> List[str]:
        '''List registered Colormaps.
        Returns
            list: list of colormap names.
        '''
        return list(self.data.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        '''Register a custom colormap.
        Args:
            custom_cmap (dict): custom colormap(s) to register.
            overwrite (bool): Overwrite existing colormap with same key. Defaults to False.
        Examples:
            >>> cmap = cmap.register({"acmap": {0: (0, 0, 0, 0), ...}})
            >>> cmap = cmap.register({"acmap": "acmap.npy"})
        '''
        data = self.data.copy()
        for name, cmap in custom_cmap.items():
            if isinstance(cmap, (str, pathlib.Path)):
                cmap = np.load(cmap).tolist()
            if name in data and not overwrite:
                raise ValueError(
                    f"Colormap {name} already exists. Use overwrite=True to overwrite.")
            data[name] = cmap
        return attr.evolve(self, data=data)

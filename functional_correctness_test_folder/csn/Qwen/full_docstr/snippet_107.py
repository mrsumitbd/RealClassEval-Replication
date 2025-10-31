
from attr import attrs, attrib
from typing import Dict, Union, List
import pathlib

ColorMapType = Dict[int, tuple]


@attrs(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data = attrib(type=Dict[str, ColorMapType], default={})

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
        new_data = self.data.copy()
        for name, cmap in custom_cmap.items():
            if name in new_data and not overwrite:
                raise ValueError(
                    f"Colormap '{name}' already exists and overwrite is False.")
            new_data[name] = cmap
        return ColorMaps(data=new_data)

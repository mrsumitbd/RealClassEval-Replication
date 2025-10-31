
import attr
from typing import Dict, List, Union
import pathlib
from rio_tiler.colormap import DEFAULTS_CMAPS, ColorMapType


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(factory=lambda: DEFAULTS_CMAPS)

    def get(self, name: str) -> ColorMapType:
        '''Fetch a colormap.
        Args:
            name (str): colormap name.
        Returns
            dict: colormap dictionary.
        '''
        return self.data.get(name)

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
            if not overwrite and name in new_data:
                continue
            if isinstance(cmap, (str, pathlib.Path)):
                # Assuming a function `parse_colormap` exists to parse colormap from file
                # For demonstration purposes, we'll just use a placeholder function
                from rio_tiler.utils import parse_colormap
                new_data[name] = parse_colormap(cmap)
            else:
                new_data[name] = cmap
        return attr.evolve(self, data=new_data)

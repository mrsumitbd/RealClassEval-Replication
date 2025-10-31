
import attr
import pathlib
from typing import Dict, List, Union, TypeVar

ColorMapType = TypeVar('ColorMapType')


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(default=attr.Factory(dict))

    def get(self, name: str) -> ColorMapType:
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
        for key, value in custom_cmap.items():
            if key in new_data and not overwrite:
                raise ValueError(
                    f"Colormap '{key}' already exists. Use overwrite=True to replace it.")
            new_data[key] = value
        return attr.evolve(self, data=new_data)

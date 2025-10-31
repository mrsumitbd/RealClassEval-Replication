
import pathlib
from typing import Dict, List, Union, TypeVar
import attr
import numpy as np

ColorMapType = TypeVar('ColorMapType', bound=Dict[int, tuple])


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(default=dict())

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
                raise ValueError(f"Colormap {name} already exists.")

            if isinstance(cmap, (str, pathlib.Path)):
                cmap_path = pathlib.Path(cmap)
                if cmap_path.suffix == '.npy':
                    cmap_data = np.load(cmap_path, allow_pickle=True).item()
                else:
                    raise ValueError("Only .npy files are supported.")
                new_data[name] = cmap_data
            else:
                new_data[name] = cmap

        return ColorMaps(data=new_data)

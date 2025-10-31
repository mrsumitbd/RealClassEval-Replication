
import attr
import pathlib
from typing import Dict, List, Union, Any

# Dummy ColorMapType for type hinting
ColorMapType = Dict[int, Any]

# Dummy DEFAULTS_CMAPS for demonstration
try:
    from rio_tiler.colormap import DEFAULTS_CMAPS
except ImportError:
    DEFAULTS_CMAPS = {
        "viridis": {0: (68, 1, 84, 255), 1: (71, 44, 122, 255)},
        "gray": {0: (0, 0, 0, 255), 1: (255, 255, 255, 255)},
    }


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(
        factory=lambda: dict(DEFAULTS_CMAPS))

    def get(self, name: str) -> ColorMapType:
        '''Fetch a colormap.
        Args:
            name (str): colormap name.
        Returns
            dict: colormap dictionary.
        '''
        if name not in self.data:
            raise KeyError(f"Colormap '{name}' not found.")
        return self.data[name]

    def list(self) -> List[str]:
        '''List registered Colormaps.
        Returns
            list: list of colormap names.
        '''
        return list(self.data.keys())

    def register(
        self,
        custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]],
        overwrite: bool = False
    ) -> 'ColorMaps':
        '''Register a custom colormap.
        Args:
            custom_cmap (dict): custom colormap(s) to register.
            overwrite (bool): Overwrite existing colormap with same key. Defaults to False.
        Examples:
            >>> cmap = cmap.register({"acmap": {0: (0, 0, 0, 0), ...}})
            >>> cmap = cmap.register({"acmap": "acmap.npy"})
        '''
        import numpy as np

        new_data = dict(self.data)
        for name, cmap in custom_cmap.items():
            if not overwrite and name in new_data:
                raise ValueError(
                    f"Colormap '{name}' already exists. Use overwrite=True to replace.")
            if isinstance(cmap, (str, pathlib.Path)):
                arr = np.load(str(cmap))
                if arr.ndim != 2 or arr.shape[1] not in (3, 4):
                    raise ValueError(
                        "Numpy colormap array must be of shape (N, 3) or (N, 4)")
                cmap_dict = {
                    int(i): tuple(map(int, arr[i])) if arr.shape[1] == 4 else tuple(map(int, arr[i])) + (255,)
                    for i in range(arr.shape[0])
                }
                new_data[name] = cmap_dict
            elif isinstance(cmap, dict):
                new_data[name] = dict(cmap)
            else:
                raise TypeError(
                    "Colormap must be a dict, str, or pathlib.Path")
        return ColorMaps(data=new_data)

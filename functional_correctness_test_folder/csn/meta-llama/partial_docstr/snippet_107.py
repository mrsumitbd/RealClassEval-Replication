
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
                # Assuming a function `read_colormap` exists to read colormap from file
                # For demonstration purposes, we'll use a placeholder function
                new_data[name] = read_colormap(cmap)
            else:
                new_data[name] = cmap
        return attr.evolve(self, data=new_data)

# Placeholder function to read colormap from file


def read_colormap(path: Union[str, pathlib.Path]) -> ColorMapType:
    # Implement your logic to read colormap from file
    # For demonstration purposes, this function is not implemented
    raise NotImplementedError("Reading colormap from file is not implemented")

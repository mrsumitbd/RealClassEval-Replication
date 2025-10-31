import attr
from rio_tiler.errors import ColorMapAlreadyRegistered, InvalidColorFormat, InvalidColorMapName, InvalidFormat
import json
import numpy
from typing import Dict, List, Sequence, Tuple, Union
import pathlib
from rio_tiler.types import ColorMapType, DataMaskType, DiscreteColorMapType, GDALColorMapType, IntervalColorMapType

@attr.s(frozen=True)
class ColorMaps:
    """Default Colormaps holder.

    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.

    """
    data: Dict[str, Union[str, pathlib.Path, ColorMapType]] = attr.ib(default=attr.Factory(lambda: DEFAULT_CMAPS_FILES))

    def get(self, name: str) -> ColorMapType:
        """Fetch a colormap.

        Args:
            name (str): colormap name.

        Returns
            dict: colormap dictionary.

        """
        cmap = self.data.get(name, None)
        if cmap is None:
            raise InvalidColorMapName(f'Invalid colormap name: {name}')
        if isinstance(cmap, (pathlib.Path, str)):
            if isinstance(cmap, str):
                cmap = pathlib.Path(cmap)
            if cmap.suffix == '.npy':
                colormap = numpy.load(cmap)
                assert colormap.shape == (256, 4)
                assert colormap.dtype == numpy.uint8
                cmap_data = {idx: tuple(value) for idx, value in enumerate(colormap)}
            elif cmap.suffix == '.json':
                with cmap.open() as f:
                    cmap_data = json.load(f, object_hook=lambda x: {int(k): parse_color(v) for k, v in x.items()})
                if isinstance(cmap_data, Sequence):
                    cmap_data = [(tuple(inter), parse_color(v)) for inter, v in cmap_data]
            else:
                raise ValueError(f'Not supported {cmap.suffix} extension for ColorMap')
            self.data[name] = cmap_data
            return cmap_data
        return cmap

    def list(self) -> List[str]:
        """List registered Colormaps.

        Returns
            list: list of colormap names.

        """
        return list(self.data)

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool=False) -> 'ColorMaps':
        """Register a custom colormap.

        Args:
            custom_cmap (dict): custom colormap(s) to register.
            overwrite (bool): Overwrite existing colormap with same key. Defaults to False.

        Examples:
            >>> cmap = cmap.register({"acmap": {0: (0, 0, 0, 0), ...}})

            >>> cmap = cmap.register({"acmap": "acmap.npy"})

        """
        for name, _ in custom_cmap.items():
            if not overwrite and name in self.data:
                raise ColorMapAlreadyRegistered(f'{name} is already registered. Use force=True to overwrite.')
        return ColorMaps({**self.data, **custom_cmap})
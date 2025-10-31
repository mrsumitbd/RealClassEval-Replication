
import json
import pathlib
from typing import Dict, List, Union

import attr
import numpy as np

from rio_tiler.colormap import DEFAULTS_CMAPS, ColorMapType


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
        if name not in self.data:
            raise KeyError(f"Colormap '{name}' not found.")
        # Return a copy to avoid accidental mutation
        return {k: tuple(v) for k, v in self.data[name].items()}

    def list(self) -> List[str]:
        '''List registered Colormaps.
        Returns
            list: list of colormap names.
        '''
        return sorted(self.data.keys())

    def register(
        self,
        custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]],
        overwrite: bool = False,
    ) -> 'ColorMaps':
        '''Register a custom colormap.
        Args:
            custom_cmap (dict): custom colormap(s) to register.
            overwrite (bool): Overwrite existing colormap with same key. Defaults to False.
        Examples:
            >>> cmap = cmap.register({"acmap": {0: (0, 0, 0, 0), ...}})
            >>> cmap = cmap.register({"acmap": "acmap.npy"})
        '''
        if not custom_cmap:
            return self

        new_data = dict(self.data)  # shallow copy

        for key, value in custom_cmap.items():
            if key in new_data and not overwrite:
                raise ValueError(
                    f"Colormap '{key}' already exists. Use overwrite=True to replace.")

            cmap: ColorMapType

            if isinstance(value, dict):
                cmap = {int(k): tuple(v) for k, v in value.items()}
            else:
                # Resolve to Path
                path = pathlib.Path(value) if not isinstance(
                    value, pathlib.Path) else value
                if not path.exists():
                    raise FileNotFoundError(
                        f"Colormap file '{path}' does not exist.")

                ext = path.suffix.lower()
                if ext == ".npy":
                    arr = np.load(path, allow_pickle=False)
                    if arr.ndim != 2 or arr.shape[1] != 4:
                        raise ValueError(
                            f"Invalid .npy format for colormap '{key}'.")
                    cmap = {i: tuple(row)
                            for i, row in enumerate(arr.tolist())}
                elif ext in {".json", ".yml", ".yaml"}:
                    with path.open("r", encoding="utf-8") as fp:
                        raw = json.load(fp)
                    cmap = {int(k): tuple(v) for k, v in raw.items()}
                else:
                    raise ValueError(
                        f"Unsupported colormap file type: '{ext}' for '{key}'.")

            new_data[key] = cmap

        return ColorMaps(data=new_data)

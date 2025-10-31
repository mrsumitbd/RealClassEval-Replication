from typing import Dict, List, Union, Mapping, Tuple
import pathlib
import json

import attr
import numpy as np

try:
    # rio-tiler >= 6
    from rio_tiler.colormap import DEFAULTS_CMAPS, ColorMapType
except Exception:  # Fallback typing if rio-tiler types are unavailable at runtime
    ColorMapType = Dict[int, Tuple[int, int, int, int]]  # type: ignore
    DEFAULTS_CMAPS = {}  # type: ignore


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(
        factory=lambda: dict(DEFAULTS_CMAPS))

    def get(self, name: str) -> ColorMapType:
        try:
            return self.data[name]
        except KeyError as exc:
            raise KeyError(f"Colormap '{name}' is not registered.") from exc

    def list(self) -> List[str]:
        '''List registered Colormaps.
        Returns
            list: list of colormap names.
        '''
        return sorted(self.data.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        '''Register a custom colormap.
        Args:
            custom_cmap (dict): custom colormap(s) to register.
            overwrite (bool): Overwrite existing colormap with same key. Defaults to False.
        Examples:
            >>> cmap = cmap.register({"acmap": {0: (0, 0, 0, 0), ...}})
            >>> cmap = cmap.register({"acmap": "acmap.npy"})
        '''
        new_data: Dict[str, ColorMapType] = dict(self.data)

        for name, value in custom_cmap.items():
            if not overwrite and name in new_data:
                raise KeyError(
                    f"Colormap '{name}' already exists. Use overwrite=True to replace it.")

            cmap: ColorMapType
            if isinstance(value, (str, pathlib.Path)):
                cmap = self._load_colormap_from_path(pathlib.Path(value))
            else:
                cmap = self._normalize_colormap_mapping(value)

            new_data[name] = cmap

        return attr.evolve(self, data=new_data)

    @staticmethod
    def _normalize_colormap_mapping(mapping: Mapping[int, Union[Tuple[int, int, int, int], List[int]]]) -> ColorMapType:
        norm: Dict[int, Tuple[int, int, int, int]] = {}
        for k, v in mapping.items():
            key = int(k)
            if isinstance(v, (list, tuple)) and len(v) == 4:
                r, g, b, a = (int(v[0]), int(v[1]), int(v[2]), int(v[3]))
                norm[key] = (r, g, b, a)
            else:
                raise ValueError(f"Invalid color tuple for index {k}: {v}")
        return norm

    @staticmethod
    def _load_colormap_from_path(path: pathlib.Path) -> ColorMapType:
        if not path.exists():
            raise FileNotFoundError(f"Colormap file not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".npy":
            arr = np.load(path)
            if arr.ndim != 2 or arr.shape[1] != 4:
                raise ValueError(
                    f"Invalid .npy colormap shape {arr.shape}; expected (N, 4).")
            arr = np.asarray(arr, dtype=np.uint8)
            return {int(i): (int(r), int(g), int(b), int(a)) for i, (r, g, b, a) in enumerate(arr)}
        elif suffix == ".json":
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(
                    "JSON colormap must be a mapping of index to RGBA.")
            # Keys might be strings in JSON; convert to int.
            return ColorMaps._normalize_colormap_mapping({int(k): v for k, v in data.items()})
        else:
            raise ValueError(
                f"Unsupported colormap file format: {path.suffix}")

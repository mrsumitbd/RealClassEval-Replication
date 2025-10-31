import os
from typing import Any, BinaryIO, Dict, Generic, Literal, Mapping, TextIO, Tuple, TypeVar, Union
import pathlib

class Loader:
    """Loader handling accessing the definitions in YAML files.

    Parameters
    ----------
    filename : Union[str, pathlib.Path]
        Path to the file to be loaded on creation.
    bundled : bool
        Is the file bundled with pyvisa-sim itself.

    """
    data: Dict[str, Any]

    def __init__(self, filename: Union[str, pathlib.Path], bundled: bool):
        self._cache = {}
        self._filename = filename
        self._bundled = bundled
        self.data = self._load(filename, bundled, SPEC_VERSION_TUPLE[0])

    def load(self, filename: Union[str, pathlib.Path], bundled: bool, parent: Union[str, pathlib.Path, None], required_version: int):
        """Load a new file into the loader.

        Parameters
        ----------
        filename : Union[str, pathlib.Path]
            Filename of the file to parse or name of the resource.
        bundled : bool
            Is the definition file bundled in pyvisa-sim.
        parent : Union[str, pathlib.Path, None]
            Path to directory in which the file can be found. If none the directory
            in which the initial file was located.
        required_version : int
            Major required version.

        """
        if self._bundled and (not bundled):
            msg = 'Only other bundled files can be loaded from bundled files.'
            raise ValueError(msg)
        if parent is None:
            parent = self._filename
        base = os.path.dirname(parent)
        filename = os.path.join(base, filename)
        return self._load(filename, bundled, required_version)

    def get_device_dict(self, device: str, filename: Union[str, pathlib.Path, None], bundled: bool, required_version: int):
        """Access a device definition.

        Parameters
        ----------
        device : str
            Name of the device information to access.
        filename : Union[str, pathlib.Path]
            Filename of the file to parse or name of the resource.
            The file must be located in the same directory as the original file.
        bundled : bool
            Is the definition file bundled in pyvisa-sim.
        required_version : int
            Major required version.

        """
        if filename is None:
            data = self.data
        else:
            data = self.load(filename, bundled, None, required_version)
        return data['devices'][device]
    _cache: Dict[Tuple[Union[str, pathlib.Path, None], bool], Dict[str, str]]
    _filename: Union[str, pathlib.Path]
    _bundled: bool

    def _load(self, filename: Union[str, pathlib.Path], bundled: bool, required_version: int) -> Dict[str, Any]:
        """Load a YAML definition file.

        The major version of the definition must match.

        """
        if (filename, bundled) in self._cache:
            return self._cache[filename, bundled]
        if bundled:
            assert isinstance(filename, str)
            data = parse_resource(filename)
        else:
            data = parse_file(filename)
        ver = _ver_to_tuple(data['spec'])[0]
        if ver != required_version:
            raise ValueError('Invalid version in %s (bundled = %s). Expected %s, found %s,' % (filename, bundled, required_version, ver))
        self._cache[filename, bundled] = data
        return data
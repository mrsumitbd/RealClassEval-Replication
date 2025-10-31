from typing import Collection, Iterable, Iterator, List, Mapping, NamedTuple, Optional
from pipask._vendor.pip._internal.exceptions import InvalidWheel, NoneMetadataError, UnsupportedWheel
from pipask._vendor.pip._vendor import pkg_resources

class InMemoryMetadata:
    """IMetadataProvider that reads metadata files from a dictionary.

    This also maps metadata decoding exceptions to our internal exception type.
    """

    def __init__(self, metadata: Mapping[str, bytes], wheel_name: Optional[str]) -> None:
        self._metadata = metadata
        self._wheel_name = wheel_name

    def has_metadata(self, name: str) -> bool:
        return name in self._metadata

    def get_metadata(self, name: str) -> str:
        try:
            return self._metadata[name].decode()
        except UnicodeDecodeError as e:
            raise UnsupportedWheel(f'Error decoding metadata for {self._wheel_name}: {e} in {name} file')

    def get_metadata_lines(self, name: str) -> Iterable[str]:
        return pkg_resources.yield_lines(self.get_metadata(name))

    def metadata_isdir(self, name: str) -> bool:
        return False

    def metadata_listdir(self, name: str) -> List[str]:
        return []

    def run_script(self, script_name: str, namespace: str) -> None:
        pass
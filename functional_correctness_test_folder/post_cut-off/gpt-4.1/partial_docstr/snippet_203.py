
from typing import Optional, List, Tuple, Set
import sys

# Dummy Tag class for demonstration; in real use, import from packaging.tags


class Tag:
    def __init__(self, interpreter, abi, platform):
        self.interpreter = interpreter
        self.abi = abi
        self.platform = platform

    def __eq__(self, other):
        return (self.interpreter, self.abi, self.platform) == (other.interpreter, other.abi, other.platform)

    def __hash__(self):
        return hash((self.interpreter, self.abi, self.platform))

    def __repr__(self):
        return f"Tag({self.interpreter!r}, {self.abi!r}, {self.platform!r})"

# Dummy get_supported function for demonstration; in real use, import from packaging.tags


def get_supported(
    version_info=None,
    platforms=None,
    abis=None,
    implementation=None
):
    # This is a stub. In real use, this would return a list of Tag objects.
    # We'll just return a list of Tag objects with the given info for demonstration.
    interpreter = implementation or "cp"
    version = ""
    if version_info:
        version = "".join(str(x) for x in version_info)
    else:
        version = f"{sys.version_info[0]}{sys.version_info[1]}"
    abis_list = abis or ["abi3"]
    platforms_list = platforms or ["any"]
    tags = []
    for plat in platforms_list:
        for abi in abis_list:
            tags.append(Tag(f"{interpreter}{version}", abi, plat))
    return tags


class TargetPython:
    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        py_version_info: Optional[Tuple[int, ...]] = None,
        abis: Optional[List[str]] = None,
        implementation: Optional[str] = None
    ) -> None:
        self.platforms = platforms
        self.py_version_info = py_version_info
        self.abis = abis
        self.implementation = implementation

    def format_given(self) -> str:
        parts = []
        if self.platforms is not None:
            parts.append(f"platforms={self.platforms}")
        if self.py_version_info is not None:
            parts.append(f"py_version_info={self.py_version_info}")
        if self.abis is not None:
            parts.append(f"abis={self.abis}")
        if self.implementation is not None:
            parts.append(f"implementation={self.implementation}")
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        return get_supported(
            version_info=self.py_version_info,
            platforms=self.platforms,
            abis=self.abis,
            implementation=self.implementation
        )

    def get_unsorted_tags(self) -> Set[Tag]:
        return set(self.get_sorted_tags())

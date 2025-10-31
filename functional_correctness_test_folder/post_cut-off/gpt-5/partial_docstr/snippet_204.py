from typing import Iterable, List, Dict, Set
import os
import re

try:
    from packaging.tags import Tag
except Exception as e:
    raise ImportError(
        "This class requires 'packaging' to be installed. pip install packaging") from e


class InvalidWheelFilename(ValueError):
    pass


class Wheel:
    '''A wheel file'''

    _build_tag_re = re.compile(r"^\d+(?:\.[A-Za-z0-9]+)?$")

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        base = os.path.basename(filename)

        if not base.endswith(".whl"):
            raise InvalidWheelFilename(
                f"Invalid wheel filename (missing .whl): {filename}")

        name = base[:-4]
        try:
            before, py, abi, plat = name.rsplit("-", 3)
        except ValueError:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (expected 4 '-' separated groups at end): {filename}")

        # Parse dist, version, optional build
        parts = before.split("-")
        if len(parts) < 2:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (missing distribution/version): {filename}")

        build = None
        if len(parts) >= 3 and self._build_tag_re.match(parts[-1]):
            build = parts[-1]
            version = parts[-2]
            dist = "-".join(parts[:-2]) if len(parts) > 2 else ""
        else:
            version = parts[-1]
            dist = "-".join(parts[:-1])

        if not dist or not version:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (empty distribution/version): {filename}")

        self.name = dist
        self.version = version
        self.build = build
        self.py_tag = py
        self.abi_tag = abi
        self.platform_tag = plat

        # Build Tag set (cartesian product of py, abi, plat)
        py_parts = py.split(".")
        abi_parts = abi.split(".")
        plat_parts = plat.split(".")

        self.file_tags: Set[Tag] = {
            Tag(p, a, pl) for p in py_parts for a in abi_parts for pl in plat_parts
        }

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(f"{t.interpreter}-{t.abi}-{t.platform}" for t in self.file_tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        index_map: Dict[Tag, int] = {t: i for i, t in enumerate(tags)}
        min_index = None
        for t in self.file_tags:
            idx = index_map.get(t)
            if idx is not None:
                if min_index is None or idx < min_index:
                    min_index = idx
        return min_index if min_index is not None else len(tags)

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        best = None
        file_tag_set = self.file_tags
        for t in tags:
            if t in file_tag_set:
                prio = tag_to_priority.get(t)
                if prio is not None and (best is None or prio < best):
                    best = prio
        return best if best is not None else len(tag_to_priority)

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        tag_set = set(tags)
        return any(t in tag_set for t in self.file_tags)

from typing import Iterable, List, Dict, Set
from itertools import product

try:
    from packaging.tags import Tag
except Exception as e:
    raise RuntimeError(
        "Wheel requires packaging to be installed: pip install packaging") from e


class InvalidWheelFilename(ValueError):
    pass


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        if not isinstance(filename, str):
            raise InvalidWheelFilename("filename must be a string")
        if not filename.endswith(".whl"):
            raise InvalidWheelFilename(
                "Invalid wheel filename (missing .whl extension)")
        self.filename = filename

        name = filename[:-4]
        parts = name.split("-")
        if len(parts) not in (5, 6):
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")

        if len(parts) == 5:
            dist, ver, py, abi, plat = parts
        else:
            dist, ver, _build, py, abi, plat = parts

        if not dist or not ver or not py or not abi or not plat:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")

        py_tags = py.split(".")
        abi_tags = abi.split(".")
        plat_tags = plat.split(".")

        if any(t == "" for t in py_tags + abi_tags + plat_tags):
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")

        self._file_tags: Set[Tag] = {
            Tag(interpreter=p, abi=a, platform=pl)
            for p, a, pl in product(py_tags, abi_tags, plat_tags)
        }

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        formatted = [
            f"{t.interpreter}-{t.abi}-{t.platform}" for t in self._file_tags]
        formatted.sort()
        return formatted

    def support_index_min(self, tags: List[Tag]) -> int:
        '''Return the lowest index that one of the wheel's file_tag combinations
        achieves in the given list of supported tags.
        For example, if there are 8 supported tags and one of the file tags
        is first in the list, then return 0.
        :param tags: the PEP 425 tags to check the wheel against, in order
            with most preferred first.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        '''
        best = None
        for i, tag in enumerate(tags):
            if tag in self._file_tags:
                best = i
                break
        if best is None:
            raise ValueError("None of the wheel's file tags are supported")
        return best

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        '''Return the priority of the most preferred tag that one of the wheel's file
        tag combinations achieves in the given list of supported tags using the given
        tag_to_priority mapping, where lower priorities are more-preferred.
        This is used in place of support_index_min in some cases in order to avoid
        an expensive linear scan of a large list of tags.
        :param tags: the PEP 425 tags to check the wheel against.
        :param tag_to_priority: a mapping from tag to priority of that tag, where
            lower is more preferred.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        '''
        best_priority = None
        for tag in self._file_tags:
            if tag in tag_to_priority:
                prio = tag_to_priority[tag]
                if best_priority is None or prio < best_priority:
                    best_priority = prio
        if best_priority is None:
            raise ValueError("None of the wheel's file tags are supported")
        return best_priority

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in self._file_tags for tag in tags)

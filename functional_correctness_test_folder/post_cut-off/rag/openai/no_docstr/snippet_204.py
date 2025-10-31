
import os
from typing import List, Dict, Iterable

from packaging.tags import Tag, parse_wheel_filename


class InvalidWheelFilename(ValueError):
    """Raised when the filename is not a valid wheel file name."""


class Wheel:
    """A wheel file."""

    def __init__(self, filename: str) -> None:
        """
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        """
        if not filename.endswith(".whl"):
            raise InvalidWheelFilename(f"Not a wheel file: {filename}")

        try:
            (
                self.distribution,
                self.version,
                self.build,
                self.python_tag,
                self.abi_tag,
                self.platform_tag,
            ) = parse_wheel_filename(os.path.basename(filename))
        except Exception as exc:
            raise InvalidWheelFilename(
                f"Invalid wheel filename: {filename}") from exc

        # Create the list of Tag objects that this wheel supports.
        # For a normal wheel there is only one tag combination.
        # For manylinux wheels, the wheel may support multiple tags; however,
        # packaging.tags does not provide a direct way to enumerate them from
        # the filename alone.  We therefore expose the single tag combination
        # that is encoded in the filename.
        self._tags: List[Tag] = [
            Tag(self.python_tag, self.abi_tag, self.platform_tag)


from typing import List, Dict, Iterable


class Wheel:
    """
    A simple representation of a Python wheel file that can parse its tags
    from the filename and provide helper methods to query support for
    specific tags.
    """

    def __init__(self, filename: str) -> None:
        """
        Initialize the Wheel with the given filename.

        Parameters
        ----------
        filename : str
            The wheel file name, e.g. "mypkg-1.0.0-py3-none-any.whl".
        """
        self.filename = filename
        # Extract tags from the filename once and cache them
        self._tags = self._extract_tags_from_filename(filename)

    def _extract_tags_from_filename(self, filename: str) -> List[str]:
        """
        Extract the tags part of a wheel filename.

        The tags are the components between the last '-' before the
        '.whl' suffix and the '.whl' suffix itself, split by '-'.

        Examples
        --------
        >>> Wheel._extract_tags_from_filename("mypkg-1.0.0-py3-none-any.whl")
        ['py3', 'none', 'any']
        """
        if not filename.endswith(".whl"):
            return []

        # Remove the .whl suffix
        core = filename[:-4]
        # Find the last '-' which separates the version from the tags
        last_dash = core.rfind('-')
        if last_dash == -1:
            return []

        tags_part = core[last_dash + 1:]
        return tags_part.split('-') if tags_part else []

    def get_formatted_file_tags(self) -> List[str]:
        """
        Return the list of tags extracted from the wheel filename.

        Returns
        -------
        List[str]
            The tags in the order they appear in the filename.
        """
        return list(self._tags)

    def support_index_min(self, tags: List[str]) -> int:
        """
        Return the minimum index of the provided tags that are supported
        by this wheel. If none of the tags are supported, return -1.

        Parameters
        ----------
        tags : List[str]
            A list of tags to check.

        Returns
        -------
        int
            The smallest index of a supported tag, or -1 if none are supported.
        """
        min_index = -1
        for idx, tag in enumerate(tags):
            if tag in self._tags:
                if min_index == -1 or idx < min_index:
                    min_index = idx
        return min_index

    def find_most_preferred_tag(
        self, tags: List[str], tag_to_priority: Dict[str, int]
    ) -> int:
        """
        Find the index of the most preferred tag among the provided tags
        based on the supplied priority mapping. Lower integer values
        indicate higher priority.

        Parameters
        ----------
        tags : List[str]
            A list of tags to evaluate.
        tag_to_priority : Dict[str, int]
            Mapping from tag to its priority value.

        Returns
        -------
        int
            The index of the tag with the highest priority that is
            supported by this wheel. If no supported tag is found,
            return -1.
        """
        best_index = -1
        best_priority = None
        for idx, tag in enumerate(tags):
            if tag not in self._tags:
                continue
            priority = tag_to_priority.get(tag)
            if priority is None:
                continue
            if best_priority is None or priority < best_priority:
                best_priority = priority
                best_index = idx
        return best_index

    def supported(self, tags: Iterable[str]) -> bool:
        """
        Determine whether any of the provided tags are supported by this wheel.

        Parameters
        ----------
        tags : Iterable[str]
            Tags to check.

        Returns
        -------
        bool
            True if at least one tag is supported, False otherwise.
        """
        return any(tag in self._tags for tag in tags)

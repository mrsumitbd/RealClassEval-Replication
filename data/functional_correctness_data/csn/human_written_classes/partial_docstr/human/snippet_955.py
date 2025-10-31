from typing import List

class IComparator:
    """Interface for a comparator which is used by :class:`ConfigurationWatcher`
    to determine if a file has been modified since the last check. A comparator
    is used to reduce the work required to reload configuration. Comparators
    should implement a mechanism that is relatively efficient (and scalable),
    so it can be performed frequently.

    :param filenames: A list of absolute paths to configuration files.
    """

    def __init__(self, filenames: List[str]) -> None:
        pass

    def has_changed(self) -> bool:
        """Returns True if any of the files have been modified since the last
        call to :func:`has_changed`. Returns False otherwise.
        """
        pass
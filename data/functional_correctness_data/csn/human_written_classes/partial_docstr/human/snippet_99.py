from typing import Any, AnyStr, BinaryIO, Callable, Dict, Generator, IO, Iterator, List, Optional, Pattern, Sequence, Tuple, TYPE_CHECKING, TypeVar, Union, cast, overload
from git.types import Files_TD, Has_id_attribute, HSH_TD, Literal, PathLike, Protocol, SupportsIndex, Total_TD, runtime_checkable

class Stats:
    """Represents stat information as presented by git at the end of a merge. It is
    created from the output of a diff operation.

    Example::

     c = Commit( sha1 )
     s = c.stats
     s.total         # full-stat-dict
     s.files         # dict( filepath : stat-dict )

    ``stat-dict``

    A dictionary with the following keys and values::

      deletions = number of deleted lines as int
      insertions = number of inserted lines as int
      lines = total number of lines changed as int, or deletions + insertions
      change_type = type of change as str, A|C|D|M|R|T|U|X|B

    ``full-stat-dict``

    In addition to the items in the stat-dict, it features additional information::

     files = number of changed files as int
    """
    __slots__ = ('total', 'files')

    def __init__(self, total: Total_TD, files: Dict[PathLike, Files_TD]) -> None:
        self.total = total
        self.files = files

    @classmethod
    def _list_from_string(cls, repo: 'Repo', text: str) -> 'Stats':
        """Create a :class:`Stats` object from output retrieved by
        :manpage:`git-diff(1)`.

        :return:
            :class:`git.Stats`
        """
        hsh: HSH_TD = {'total': {'insertions': 0, 'deletions': 0, 'lines': 0, 'files': 0}, 'files': {}}
        for line in text.splitlines():
            change_type, raw_insertions, raw_deletions, filename = line.split('\t')
            insertions = raw_insertions != '-' and int(raw_insertions) or 0
            deletions = raw_deletions != '-' and int(raw_deletions) or 0
            hsh['total']['insertions'] += insertions
            hsh['total']['deletions'] += deletions
            hsh['total']['lines'] += insertions + deletions
            hsh['total']['files'] += 1
            files_dict: Files_TD = {'insertions': insertions, 'deletions': deletions, 'lines': insertions + deletions, 'change_type': change_type}
            hsh['files'][filename.strip()] = files_dict
        return Stats(hsh['total'], hsh['files'])
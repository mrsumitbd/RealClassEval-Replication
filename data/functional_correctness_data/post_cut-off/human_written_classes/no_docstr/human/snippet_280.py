from pipask._vendor.pip._internal.utils.compat import WINDOWS
from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Set, Tuple
import os

class UninstallPthEntries:

    def __init__(self, pth_file: str) -> None:
        self.file = pth_file
        self.entries: Set[str] = set()
        self._saved_lines: Optional[List[bytes]] = None

    def add(self, entry: str) -> None:
        entry = os.path.normcase(entry)
        if WINDOWS and (not os.path.splitdrive(entry)[0]):
            entry = entry.replace('\\', '/')
        self.entries.add(entry)

    def remove(self) -> None:
        logger.verbose('Removing pth entries from %s:', self.file)
        if not os.path.isfile(self.file):
            logger.warning('Cannot remove entries from nonexistent file %s', self.file)
            return
        with open(self.file, 'rb') as fh:
            lines = fh.readlines()
            self._saved_lines = lines
        if any((b'\r\n' in line for line in lines)):
            endline = '\r\n'
        else:
            endline = '\n'
        if lines and (not lines[-1].endswith(endline.encode('utf-8'))):
            lines[-1] = lines[-1] + endline.encode('utf-8')
        for entry in self.entries:
            try:
                logger.verbose('Removing entry: %s', entry)
                lines.remove((entry + endline).encode('utf-8'))
            except ValueError:
                pass
        with open(self.file, 'wb') as fh:
            fh.writelines(lines)

    def rollback(self) -> bool:
        if self._saved_lines is None:
            logger.error('Cannot roll back changes to %s, none were made', self.file)
            return False
        logger.debug('Rolling %s back to previous state', self.file)
        with open(self.file, 'wb') as fh:
            fh.writelines(self._saved_lines)
        return True
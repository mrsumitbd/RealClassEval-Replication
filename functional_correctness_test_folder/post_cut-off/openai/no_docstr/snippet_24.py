
import re
from typing import List
from urllib.parse import urlparse


class LocalPathExtractor:
    @staticmethod
    def is_local_path(path: str) -> bool:
        """
        Return True if the given path string represents a local filesystem path.
        A path is considered local if it has no scheme and no network location.
        """
        parsed = urlparse(path)
        return not parsed.scheme and not parsed.netloc

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        """
        Extract all local filesystem paths from the given text.
        Paths are identified by the presence of slashes or backslashes and
        are filtered to ensure they are local (no URL scheme).
        """
        # Regex to match typical local paths:
        #   - Windows absolute paths like C:\folder\file
        #   - Unix absolute paths starting with /
        #   - Relative paths starting with ./ or ../
        #   - Other paths containing slashes/backslashes
        pattern = r"""
            (?<!\w)                                   # not preceded by a word char
            (?:                                       # start non-capturing group
                [A-Za-z]:\\[^\s'"]+                  # Windows absolute path
                |                                     # or
                /[^\s'"]+                             # Unix absolute path
                |                                     # or
                \.{1,2}/[^\s'"]+                      # relative path
                |                                     # or
                [^\s'"]*[\\/][^\s'"]+                 # any path containing slash/backslash
            )
        """
        raw_paths = re.findall(pattern, text, re.VERBOSE)
        # Filter out any that are actually URLs
        local_paths = [
            p for p in raw_paths if LocalPathExtractor.is_local_path(p)]
        return local_paths

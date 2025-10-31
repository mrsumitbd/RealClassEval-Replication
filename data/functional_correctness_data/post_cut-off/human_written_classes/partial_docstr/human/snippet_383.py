from collections import defaultdict
from packaging.utils import InvalidSdistFilename, InvalidVersion, InvalidWheelFilename, canonicalize_name, parse_sdist_filename, parse_wheel_filename
import os
from pipask._vendor.pip._internal.utils.urls import path_to_url, url_to_path
from typing import Callable, Dict, Iterable, List, Optional, Tuple

class _FlatDirectoryToUrls:
    """Scans directory and caches results"""

    def __init__(self, path: str) -> None:
        self._path = path
        self._page_candidates: List[str] = []
        self._project_name_to_urls: Dict[str, List[str]] = defaultdict(list)
        self._scanned_directory = False

    def _scan_directory(self) -> None:
        """Scans directory once and populates both page_candidates
        and project_name_to_urls at the same time
        """
        for entry in os.scandir(self._path):
            url = path_to_url(entry.path)
            if _is_html_file(url):
                self._page_candidates.append(url)
                continue
            try:
                project_filename = parse_wheel_filename(entry.name)[0]
            except (InvalidWheelFilename, InvalidVersion):
                try:
                    project_filename = parse_sdist_filename(entry.name)[0]
                except (InvalidSdistFilename, InvalidVersion):
                    continue
            self._project_name_to_urls[project_filename].append(url)
        self._scanned_directory = True

    @property
    def page_candidates(self) -> List[str]:
        if not self._scanned_directory:
            self._scan_directory()
        return self._page_candidates

    @property
    def project_name_to_urls(self) -> Dict[str, List[str]]:
        if not self._scanned_directory:
            self._scan_directory()
        return self._project_name_to_urls
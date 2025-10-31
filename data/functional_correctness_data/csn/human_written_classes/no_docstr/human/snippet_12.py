import sys
from pathlib import Path
from copy import copy

class _patch_import_path_for_repo:

    def __init__(self, repo_dir: Path | str) -> None:
        self._repo_dir = f'{repo_dir}' if isinstance(repo_dir, Path) else repo_dir

    def __enter__(self) -> None:
        self._path = copy(sys.path)
        sys.path.append(self._repo_dir)

    def __exit__(self, _type, _value, _traceback):
        sys.path = self._path
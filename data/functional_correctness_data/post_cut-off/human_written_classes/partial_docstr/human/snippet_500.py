from filelock import FileLock
from dataclasses import dataclass, field
import subprocess
from os import PathLike
from pathlib import Path
from lean_interact.utils import DEFAULT_CACHE_DIR, _GitUtilities, check_lake, get_project_lean_version, logger

@dataclass(frozen=True, kw_only=True)
class BaseProject:
    """Base class for Lean projects"""
    directory: str | PathLike | None
    lake_path: str | PathLike = 'lake'
    'The path to the lake executable. Default is "lake", which assumes it is in the system PATH.'
    auto_build: bool = True
    'Whether to automatically build the project after instantiation.'

    def __post_init__(self):
        if self.auto_build:
            self.build()

    def get_directory(self) -> str:
        """Get the directory of the Lean project."""
        if self.directory is None:
            raise ValueError('`directory` must be set')
        return str(Path(self.directory).resolve())

    def get_lean_version(self) -> str:
        """The Lean version used by this project."""
        version = get_project_lean_version(Path(self.get_directory()))
        if version is None:
            raise ValueError('Unable to determine Lean version')
        return version

    def build(self, verbose: bool=True, update: bool=False, _lock: bool=True) -> None:
        """Build the Lean project using lake.
        Args:
            verbose: Whether to print building information to the console.
            update: Whether to run `lake update` before building.
            _lock: (internal parameter) Whether to acquire a file lock (should be False if already locked by caller).
        """
        directory = Path(self.get_directory())
        check_lake(self.lake_path)

        def _do_build():
            stdout = None if verbose else subprocess.DEVNULL
            stderr = None if verbose else subprocess.DEVNULL
            try:
                if update:
                    subprocess.run([str(self.lake_path), 'update'], cwd=directory, check=True, stdout=stdout, stderr=stderr)
                cache_result = subprocess.run([str(self.lake_path), 'exe', 'cache', 'get'], cwd=directory, check=False, stdout=stdout, stderr=stderr)
                if cache_result.returncode != 0 and verbose:
                    logger.info("Getting 'error: unknown executable cache' is expected if the project doesn't depend on Mathlib")
                subprocess.run([str(self.lake_path), 'build'], cwd=directory, check=True, stdout=stdout, stderr=stderr)
                logger.debug('Successfully built project at %s', directory)
            except subprocess.CalledProcessError as e:
                logger.error('Failed to build the project: %s', e)
                raise
        if _lock:
            with FileLock(f'{directory}.lock'):
                _do_build()
        else:
            _do_build()
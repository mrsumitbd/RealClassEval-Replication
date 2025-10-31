from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union
from pathlib import Path
from tempfile import NamedTemporaryFile

class _TempFile:
    """Proxy class to workaround errors on Windows."""

    def __enter__(self) -> '_TempFile':
        with NamedTemporaryFile(prefix='lightgbm_tmp_', delete=True) as f:
            self.name = f.name
            self.path = Path(self.name)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.path.is_file():
            self.path.unlink()
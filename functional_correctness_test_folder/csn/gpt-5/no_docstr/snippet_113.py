from pathlib import Path
import builtins
from typing import Union, IO, AnyStr, Optional


class FileLikeIO:
    def open(self, path: Union[str, Path], mode: str = 'r') -> IO[AnyStr]:
        p = Path(path)
        if any(flag in mode for flag in ('w', 'a', 'x', '+')):
            parent = p.parent
            if parent and not parent.exists():
                parent.mkdir(parents=True, exist_ok=True)
        if 'b' in mode:
            return builtins.open(p, mode)
        return builtins.open(p, mode, encoding='utf-8', newline='')

    def exists(self, path: Union[str, Path]) -> bool:
        return Path(path).exists()

    def remove(self, path: Union[str, Path]) -> None:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(str(p))
        if p.is_dir():
            raise IsADirectoryError(str(p))
        p.unlink()

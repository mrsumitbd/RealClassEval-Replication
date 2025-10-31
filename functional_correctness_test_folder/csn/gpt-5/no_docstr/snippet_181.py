import os
import io
from pathlib import Path
from typing import Dict, List, Optional


class BaseLoader:
    def __init__(self, root: Optional[os.PathLike] = None, extensions: Optional[List[str]] = None, encoding: str = "utf-8"):
        self.root = Path(root or ".").resolve()
        self.extensions = set(e.lower() if e.startswith(
            ".") else f".{e.lower()}" for e in (extensions or [])) or None
        self.encoding = encoding
        self._index: Dict[str, List[Path]] = {}
        self._cache: Dict[Path, str] = {}
        self._indexed = False

    def _ensure_index(self):
        if self._indexed:
            return
        for path in self.fetchFiles():
            name = path.name
            stem = path.stem
            self._index.setdefault(name.lower(), []).append(path)
            self._index.setdefault(stem.lower(), []).append(path)
        self._indexed = True

    def getTextForName(self, query_name):
        if not isinstance(query_name, str) or not query_name.strip():
            raise ValueError("query_name must be a non-empty string")

        self._ensure_index()

        q = query_name.strip()
        qp = Path(q)
        if qp.is_absolute() or any(sep in q for sep in (os.sep, os.altsep) if sep):
            target = (qp if qp.is_absolute() else (self.root / qp)).resolve()
            if not target.exists() or not target.is_file():
                raise FileNotFoundError(f"No such file: {target}")
            return self._getText(str(target))

        candidates = self._index.get(q.lower(), [])
        if not candidates:
            raise FileNotFoundError(
                f"No files found matching name or stem: {q}")

        exact = [p for p in candidates if p.name.lower() == q.lower()]
        if len(exact) == 1:
            return self._getText(str(exact[0]))
        if len(candidates) == 1:
            return self._getText(str(candidates[0]))

        dedup = []
        seen = set()
        for p in candidates:
            if p not in seen:
                seen.add(p)
                dedup.append(p)

        raise ValueError(
            f"Ambiguous query_name '{q}'; matches: {', '.join(str(p) for p in dedup)}")

    def _getText(self, queryFullName):
        path = Path(queryFullName)
        if not path.is_absolute():
            path = (self.root / path).resolve()

        if path in self._cache:
            return self._cache[path]

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"No such file: {path}")

        with io.open(path, "r", encoding=self.encoding, errors="replace") as f:
            text = f.read()

        self._cache[path] = text
        return text

    def fetchFiles(self):
        files = []
        if not self.root.exists() or not self.root.is_dir():
            return files
        for dirpath, _, filenames in os.walk(self.root):
            for fname in filenames:
                p = Path(dirpath) / fname
                if self.extensions is not None:
                    if p.suffix.lower() not in self.extensions:
                        continue
                files.append(p.resolve())
        return files

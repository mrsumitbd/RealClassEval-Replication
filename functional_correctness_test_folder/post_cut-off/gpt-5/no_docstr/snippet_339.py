from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional, Union, Iterable


class MCPConfigGenerator:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir).expanduser(
        ).resolve() if base_dir else None
        self._vars: Dict[str, str] = {}
        if self.base_dir:
            self._vars["BASE_DIR"] = str(self.base_dir)

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(config, dict):
            raise TypeError("config must be a dict")
        data = deepcopy(config)
        return self._transform(data)

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        out_path = Path(output_path).expanduser()
        if not out_path.suffix:
            out_path = out_path.with_suffix(".json")
        out_path = out_path.resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        processed = self.generate_config(config)

        tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(processed, f, indent=2, ensure_ascii=False)
            f.write("\n")
        tmp_path.replace(out_path)

    # Internal helpers

    def _transform(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {k: self._transform(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._transform(v) for v in value]
        if isinstance(value, tuple):
            return tuple(self._transform(v) for v in value)
        if isinstance(value, (set, frozenset)):
            return type(value)(self._transform(v) for v in value)
        if isinstance(value, str):
            return self._process_string(value)
        return value

    def _process_string(self, s: str) -> str:
        s = self._expand_vars(s)
        if self._looks_like_path(s):
            return self._normalize_path(s)
        return s

    def _expand_vars(self, s: str) -> str:
        if self._vars:
            for k, v in self._vars.items():
                s = s.replace(f"${{{k}}}", v)
        s = os.path.expanduser(s)
        s = os.path.expandvars(s)
        return s

    def _looks_like_path(self, s: str) -> bool:
        if not s:
            return False
        if s.startswith(("./", "../", "/")):
            return True
        if self.base_dir and not ("://" in s):
            if any(sep in s for sep in ("/", "\\")):
                return True
        if s.startswith("."):
            return True
        return False

    def _normalize_path(self, s: str) -> str:
        p = Path(s)
        if not p.is_absolute() and self.base_dir:
            p = self.base_dir / p
        try:
            p = p.resolve()
        except Exception:
            p = p.expanduser()
        return str(p)

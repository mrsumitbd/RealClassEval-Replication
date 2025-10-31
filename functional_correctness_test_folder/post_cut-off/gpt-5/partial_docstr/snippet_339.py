from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = Path(base_dir).expanduser(
        ).resolve() if base_dir else Path.cwd()

    def _resolve_path_value(self, value: str) -> str:
        expanded = os.path.expandvars(os.path.expanduser(value))
        p = Path(expanded)
        if p.is_absolute():
            return str(p)
        return str((self.base_dir / p).resolve())

    def _process(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            out: Dict[str, Any] = {}
            for k, v in obj.items():
                if isinstance(v, str) and (k == "path" or k == "cwd" or k.endswith("_path")):
                    out[k] = self._resolve_path_value(v)
                else:
                    out[k] = self._process(v)
            return out
        if isinstance(obj, list):
            return [self._process(item) for item in obj]
        return obj

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")
        return self._process(config)

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        processed = self.generate_config(config)
        out_path = Path(output_path).expanduser()
        if not out_path.is_absolute():
            out_path = (self.base_dir / out_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(processed, f, indent=2,
                      sort_keys=True, ensure_ascii=False)

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Union


class WorkflowDefinition:
    NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.\- ]+$")

    def __init__(self, name: str, file_path: Union[str, os.PathLike], metadata: Optional[Dict[str, Any]], content: Union[str, bytes]):
        self.name = name
        self.file_path = Path(file_path) if file_path is not None else None
        self.metadata = dict(metadata) if metadata is not None else {}
        self.content = content.decode(
            "utf-8") if isinstance(content, (bytes, bytearray)) else content

    def validate(self) -> bool:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if not self.NAME_PATTERN.match(self.name.strip()):
            raise ValueError("name contains invalid characters")

        if self.file_path is None or not isinstance(self.file_path, Path):
            raise ValueError("file_path must be a valid path")
        if not self.file_path.exists():
            raise ValueError(f"file_path does not exist: {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"file_path is not a file: {self.file_path}")

        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dict")
        for k in self.metadata.keys():
            if not isinstance(k, str) or not k:
                raise ValueError("metadata keys must be non-empty strings")
        # Ensure metadata is JSON serializable
        try:
            json.dumps(self.metadata)
        except Exception as e:
            raise ValueError(f"metadata must be JSON-serializable: {e}")

        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content must be a non-empty string")

        # Ensure file is readable
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                _ = f.read(1)
        except Exception as e:
            raise ValueError(f"file_path is not readable: {e}")

        return True

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
import json
from pathlib import Path


@dataclass
class TemplateFile:
    content: str = ""
    context: Dict[str, Any] = field(default_factory=dict)

    def save(self, file_name: str):
        path = Path(file_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "content": self.content,
            "context": self.context,
        }
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def from_file(cls, file_name: str):
        path = Path(file_name)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            content=data.get("content", ""),
            context=data.get("context", {}),
        )

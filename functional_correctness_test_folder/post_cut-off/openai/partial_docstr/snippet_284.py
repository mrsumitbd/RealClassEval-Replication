
from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Union


@dataclass
class UpdateFeedModel:
    # Example fields – adjust as needed
    feed_id: int
    details: Union[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Convert string details to dict if needed."""
        if isinstance(self.details, str):
            # Try to parse as JSON first
            try:
                parsed = json.loads(self.details)
                if isinstance(parsed, dict):
                    self.details = parsed
                    return
            except json.JSONDecodeError:
                pass

            # Fallback: parse comma‑separated key=value pairs
            details_dict: Dict[str, Any] = {}
            for part in self.details.split(","):
                part = part.strip()
                if not part:
                    continue
                if "=" in part:
                    key, value = part.split("=", 1)
                    details_dict[key.strip()] = value.strip()
                else:
                    details_dict[part] = True
            self.details = details_dict

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the model."""
        return asdict(self)

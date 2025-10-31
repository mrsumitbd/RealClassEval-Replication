from dataclasses import dataclass, field, fields
from typing import Any, Dict, Optional, Union
from collections.abc import Mapping
import json
import ast


@dataclass
class CreateFeedModel:
    details: Optional[Union[str, Dict[str, Any]]] = None

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            raw = self.details.strip()
            if not raw:
                self.details = None
                return
            # Try JSON first
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    self.details = parsed
                    return
            except Exception:
                pass
            # Fallback to Python literal eval for dict-like strings
            try:
                parsed = ast.literal_eval(raw)
                if isinstance(parsed, dict):
                    self.details = parsed
                    return
            except Exception:
                pass
            # Leave as original string if not a dict

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        result: Dict[str, Any] = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            # Shallow copy dict-like to avoid external mutation side effects
            if isinstance(value, Mapping):
                result[f.name] = dict(value)
            else:
                result[f.name] = value
        return result

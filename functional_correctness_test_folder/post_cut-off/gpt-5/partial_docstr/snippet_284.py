from dataclasses import dataclass
from typing import Any, Dict, Union, Optional
import json


@dataclass
class UpdateFeedModel:
    details: Union[str, Dict[str, Any], None] = None

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            s = self.details.strip()
            if not s:
                self.details = {}
                return
            try:
                parsed = json.loads(s)
                if isinstance(parsed, dict):
                    self.details = parsed
                else:
                    self.details = {"value": parsed}
            except Exception:
                tentative: Dict[str, Any] = {}
                try:
                    parts = [p.strip() for p in s.replace(
                        ";", ",").split(",") if p.strip()]
                    for p in parts:
                        if "=" in p:
                            k, v = p.split("=", 1)
                            tentative[k.strip()] = v.strip()
                except Exception:
                    pass
                self.details = tentative if tentative else {"value": s}
        elif self.details is None:
            self.details = {}

    def to_dict(self) -> Dict[str, Any]:
        return {"details": self.details}

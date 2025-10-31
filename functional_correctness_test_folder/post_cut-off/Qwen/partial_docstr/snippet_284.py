
from dataclasses import dataclass, field
from typing import Any, Dict, Union


@dataclass
class UpdateFeedModel:
    details: Union[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.details, str):
            try:
                self.details = eval(self.details)
            except (SyntaxError, NameError):
                self.details = {}

    def to_dict(self) -> Dict[str, Any]:
        return {'details': self.details}


from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Optional, List


@dataclass
class UpdateFeedModel:
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.id is not None:
            self.id = int(self.id)
        if self.updated_at is not None and not isinstance(self.updated_at, str):
            self.updated_at = str(self.updated_at)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

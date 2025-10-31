from dataclasses import dataclass, field
from typing import Iterable, Optional

@dataclass
class Section:
    name: str
    checks: list = field(default_factory=list)
    description: Optional[str] = None

    def __repr__(self):
        return f'<Section: {self.name}>'

    def has_check(self, check_id):
        return any((check.id == check_id for check in self.checks))
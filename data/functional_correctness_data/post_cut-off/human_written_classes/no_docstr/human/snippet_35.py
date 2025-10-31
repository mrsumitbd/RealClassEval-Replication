from dataclasses import dataclass
from typing import Any, Generator

@dataclass
class Chapter:
    id: int
    name: str
    children: list['Chapter']

    def __iter__(self) -> Generator['Chapter', None, None]:
        for child in self.children:
            yield child
            yield from child

    def json(self) -> dict[str, Any]:
        return {'id': self.id, 'headline': self.name, 'children': [child.json() for child in self.children]}
from uuid import UUID
from typing import Optional, Any, Literal, Union
from dataclasses import dataclass, field

@dataclass
class Wiki:
    text: str
    version: int = 0
    _dataset_id: Union[UUID, None] = None
    _dremio: Any = None

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return self.text

    def commit(self) -> 'Wiki':
        return self._dremio.set_wiki(self._dataset_id, self, True)
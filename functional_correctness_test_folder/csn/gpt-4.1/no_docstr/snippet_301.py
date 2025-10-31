
from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class BaseFitResult:
    _correlation_matrix: Dict[Tuple[str, str],
                              float] = field(default_factory=dict)

    @property
    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        return self._correlation_matrix

    @correlation_matrix.setter
    def correlation_matrix(self, value: dict[tuple[str, str], float]):
        self._correlation_matrix = value

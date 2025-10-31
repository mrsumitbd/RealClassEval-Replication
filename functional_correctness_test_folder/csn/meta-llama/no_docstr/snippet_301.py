
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class BaseFitResult:
    _correlation_matrix: Dict[Tuple[str, str], float] = None

    @property
    def correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        return self._correlation_matrix

    @correlation_matrix.setter
    def correlation_matrix(self, value: Dict[Tuple[str, str], float]) -> None:
        self._correlation_matrix = value

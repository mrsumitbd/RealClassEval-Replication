
from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class BaseFitResult:
    _correlation_matrix: Dict[Tuple[str, str],
                              float] = field(default_factory=dict)

    @property
    def correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        return self._correlation_matrix

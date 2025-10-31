
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class BaseFitResult:
    @property
    def correlation_matrix(self) -> Dict[Tuple[str, str], float]:
        pass

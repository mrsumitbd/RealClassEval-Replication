
from dataclasses import dataclass


@dataclass
class BaseFitResult:
    @property
    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        pass

    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        pass

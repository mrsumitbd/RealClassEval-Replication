from dataclasses import dataclass, field
from typing import Dict, Tuple, Mapping


@dataclass
class BaseFitResult:
    _correlation_matrix: Dict[Tuple[str, str],
                              float] = field(default_factory=dict)

    @property
    def correlation_matrix(self) -> dict[tuple[str, str], float]:
        return self._correlation_matrix

    @correlation_matrix.setter
    def correlation_matrix(self, value: Mapping[Tuple[str, str], float]) -> None:
        if value is None:
            self._correlation_matrix = {}
            return
        if not isinstance(value, Mapping):
            raise TypeError(
                "correlation_matrix must be a mapping of (str, str) to float")
        cm: Dict[Tuple[str, str], float] = {}
        for k, v in value.items():
            if not (isinstance(k, tuple) and len(k) == 2 and all(isinstance(x, str) for x in k)):
                raise TypeError("All keys must be 2-tuples of strings")
            try:
                fv = float(v)
            except Exception as e:
                raise TypeError(
                    "All values must be convertible to float") from e
            cm[(k[0], k[1])] = fv
        self._correlation_matrix = cm

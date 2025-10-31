
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class EvaluationResult:
    """
    Result of program evaluation containing both metrics and optional artifacts.
    This maintains backward compatibility with the existing dict[str, float] contract
    while adding a side‑channel for arbitrary artifacts (text or binary data).

    IMPORTANT: For custom MAP‑Elites features, metrics values must be raw continuous
    scores (e.g., actual counts, percentages, continuous measurements), NOT pre‑computed
    bin indices. The database handles all binning internally using min‑max scaling.
    """
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, bytes] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        """
        Auto‑wrap dict returns for backward compatibility.
        """
        return cls(metrics=metrics, artifacts={})

    def to_dict(self) -> Dict[str, float]:
        """
        Backward compatibility – return just metrics.
        """
        return dict(self.metrics)

    def has_artifacts(self) -> bool:
        """
        Check if this result contains any artifacts.
        """
        return bool(self.artifacts)

    def get_artifact_keys(self) -> List[str]:
        """
        Get list of artifact keys.
        """
        return list(self.artifacts.keys())

    def get_artifact_size(self, key: str) -> int:
        """
        Get size of a specific artifact in bytes.
        """
        data = self.artifacts.get(key)
        return len(data) if data is not None else 0

    def get_total_artifact_size(self) -> int:
        """
        Get total size of all artifacts in bytes.
        """
        return sum(len(v) for v in self.artifacts.values())
